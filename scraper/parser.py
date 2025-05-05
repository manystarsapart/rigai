import os
import csv
from bs4 import BeautifulSoup

'''
td__name -> Name
td__spec--i -> Spec i (unique for each product)
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

# product specs
CPU_HEADERS = [
    "core_count",
    "performance_core_clock",
    "performance_core_boost_clock",
    "microarchitecture",
    "tdp",
    "integrated_graphics"
]

CPU_COOLER_HEADERS = [
    "fan_rpm",
    "noise_level",
    "color",
    "radiator_size"
]

MOTHERBOARD_HEADERS = [
    "cpu_socket",
    "form_factor",
    "max_memory",
    "memory_slots",
    "color"
]

MEMORY_HEADERS = [
    "speed",
    "modules",
    "price_per_gb",
    "color",
    "first_word_latency",
    "cas_latency"
]

INTERNAL_HARD_DRIVE_HEADERS = [
    "capacity",
    "price_per_gb",
    "type",
    "cache",
    "form_factor",
    "interface"
]

VIDEO_CARD_HEADERS = [
    "chipset",
    "memory",
    "core_clock",
    "boost_clock",
    "color",
    "length"
]

POWER_SUPPLY_HEADERS = [
    "type",
    "efficiency_rating",
    "wattage",
    "modular",
    "color"
]

CASE_HEADERS = [
    "type",
    "color",
    "power_supply",
    "side_panel",
    "external_volume",
    "internal_bays"
]

def ensure_text(cell, tag=None):
    if not cell:
        return "None"
    text = cell.get_text(strip=True) if cell else "None"
    return text if text else "None"

def get_product_details(rows, spec_count, spec_headers):
    '''
    Input:
    - rows: <tr> rows parsed by BeautifulSoup4
    - spec_count: no. of specs unique to product
    - headers: fields of product, in the format [title, ..., ..., rating, price]

    Output:
    - products: list of products formatted as a header:value dictionary
    '''
    products = []

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
        for i in range(1, spec_count+1):
            spec_cell = row.find('td', class_=f'td__spec--{i}')
            cls = spec_cell.get('class', [])
            if 'td--empty' in cls:
                specs.append("None")
            else:
                for h6 in spec_cell.find_all("h6"):
                    h6.extract()
                specs.append(ensure_text(spec_cell))

        title = ensure_text(title_cell)
        price = ensure_text(price_cell)

        product = ({
            'title': title,
            'rating': rating,
            'price': price
        })

        for i in range(len(spec_headers)):
            spec = spec_headers[i]
            product[spec] = specs[i]

        products.append(product)

    return products

def scrape_product(product_name, spec_headers):
    data_path = f"./data/{product_name}.csv"
    pages_path = f"./pages/{product_name}"

    pages = len(os.listdir(pages_path))
    headers = [
        'title',
        'rating',
        'price'
    ] + spec_headers

    # write header row
    with open(data_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()

    for i in range(1, pages+1):
        with open(f"{pages_path}/page{i}.txt", "rb") as f:
            response = f.read()
        soup = BeautifulSoup(str(response), 'html.parser')
        rows = soup.find_all('tr', class_='tr__product')

        products = get_product_details(rows, len(spec_headers), spec_headers)

        with open(data_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, headers)
            writer.writerows(products)

if __name__ == "__main__":
    '''
    Possible product names:
    - case
    - cpu
    - cpu-cooler
    - internal-hard-drive
    - memory
    - motherboard
    - power-supply
    - video-card
    '''
    scrape_product("motherboard", MOTHERBOARD_HEADERS)