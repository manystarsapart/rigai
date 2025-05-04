import os
import time
from dotenv import load_dotenv
from tqdm import tqdm
from firecrawl import FirecrawlApp, ScrapeOptions 

load_dotenv()
APIKEY = os.getenv("APIKEY")

def scrape_all(product, pages):
    for i in tqdm(range(16, pages+1), desc="Scraping pages"):
        app = FirecrawlApp(api_key=APIKEY)
        response = app.scrape_url(f'https://pcpartpicker.com/products/{product}/#page={i}', formats=['html'])
        with open(f"./pages/{product}/page{i}.txt", "w") as f:
            f.write(str(response))
            f.close()

def scrape_one(product, page):
    app = FirecrawlApp(api_key=APIKEY)
    i = page
    response = app.scrape_url(f'https://pcpartpicker.com/products/{product}/#page={i}', formats=['html'])
    with open(f"./pages/{product}/page{i}.txt", "w") as f:
        f.write(str(response))
        f.close()

start = time.time()
print("Starting to scrape...")

scrape_one("cpu-cooler", 19)

end = time.time()
print(f"Done! Time elapsed: {round(end-start, 3)}s")