import csv
from bs4 import BeautifulSoup

'''
Some notes:

td__name -> Name
td__spec--1 -> Core Count
td__spec--2 -> Performance Core Clock
td__spec--3 -> Performance Core Boost Clock
td__spec--4 -> Microarchitecture
td__spec--5 -> TDP
td__spec--6 -> Integrated Graphics
td__rating -> Rating
td__price -> Price

For Rating,
- <td> contains a <ul class="product--rating">
- which contains <li> elements of one of three:
1. <svg class="shape-star-full">
2. <svg class="shape-star-half">
3. <svg class="shape-star-empty">

Some <tds> may also have class="td--empty".
'''

def ensure_text(cell, tag=None):
    if not cell:
        return "None"
    text = cell.get_text(strip=True) if cell else "None"
    return text if text else "None"

def get_cpu_details(rows):
    cpus = []

    for row in rows:
        title_cell = row.find('td', class_='td__name')
        price_cell = row.find('td', class_='td__price')
        rating_cell = row.find('td', class_='td__rating')

        # extract title from <p> tag
        title_cell = title_cell.find('p')

        # remove button from price cell
        if price_cell:
            [btn.extract() for btn in price_cell.find_all("button")]

        # parse numerical rating from rating cell
        if '(0)' in rating_cell.get_text():
            rating = "None"
        else:
            rating = 0.0
            for svg in rating_cell.find_all('svg'):
                cls = svg.get('class', [])
                if 'shape-star-full' in cls:
                    rating += 1.0
                elif 'shape-star-half' in cls:
                    rating += 0.5

        # extract spec values
        specs = []
        for i in range(1, 7):
            spec_cell = row.find('td', class_=f'td__spec--{i}')
            for h6 in spec_cell.find_all("h6"):
                h6.extract()
            specs.append(ensure_text(spec_cell))

        title = ensure_text(title_cell)
        price = ensure_text(price_cell)
        spec1, spec2, spec3, spec4, spec5, spec6 = specs

        cpus.append({
            'title': title,
            'core_count': spec1,
            'performance_core_clock': spec2,
            'performance_core_boost_clock': spec3,
            'microarchitecture': spec4,
            'tdp': spec5,
            'integrated_graphics': spec6,
            'rating': rating,
            'price': price
        })

    return cpus

def scrape_cpu():
    pages = 15
    headers = [
        'title',
        'core_count',
        'performance_core_clock',
        'performance_core_boost_clock',
        'microarchitecture',
        'tdp',
        'integrated_graphics',
        'rating',
        'price'
    ]

    # write header row
    with open('cpus.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()

    for i in range(1, pages+1):
        with open(f"./pages/page{i}.txt", "rb") as f:
            response = f.read()
        soup = BeautifulSoup(str(response), 'html.parser')
        cpu_rows = soup.find_all('tr', class_='tr__product')

        cpus = get_cpu_details(rows=cpu_rows)

        with open('cpus.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, headers)
            writer.writerows(cpus)

if __name__ == "__main__":
    scrape_cpu()