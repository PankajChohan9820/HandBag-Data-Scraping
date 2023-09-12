from bs4 import BeautifulSoup as bs
import time
import helper
import warnings
from typing import List

# Ignore warnings
warnings.filterwarnings("ignore")

def product_links() -> List[str]:
    """
    Scrapes product links from the Vestiaire Collective website.

    Returns:
    - List[str]: List of product URLs.
    """
    driver = helper.get_webdriver()
    # Get the list of all products
    product_links = []
    try:
        for page in range(1, 3):  # Scraping pages 1 and 2
            if page == 1:
                url = 'https://us.vestiairecollective.com/women-bags/'
            else:
                url = 'https://us.vestiairecollective.com/women-bags/p-{}/'.format(page)
            driver.get(url)
            SCROLL_PAUSE_TIME = 2  # Pause time between scrolls
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            soup = bs(driver.page_source, "html.parser")
            product_ul = soup.find("ul", class_="product-search_catalog__flexContainer__Dg0eL")
            if product_ul:
                products = product_ul.find_all("li")
                for j in range(len(products)):
                    p = products[j]
                    link = p.findAll('a')
                    pages = link[0]['href']
                    product_links.append(pages)
        return product_links
    except Exception as e:
        return []  # Return an empty list in case of an error
