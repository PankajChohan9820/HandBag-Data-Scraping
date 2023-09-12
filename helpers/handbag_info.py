from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
from typing import Dict

# Ignore warnings
warnings.filterwarnings("ignore")

# Using BeautifulSoup to extract general information from HTML
def general_information(html: str) -> Dict[str, str]:
    """
    Extracts general product information from HTML using BeautifulSoup.

    Args:
    - html (str): The HTML content of the product page.

    Returns:
    - Dict[str, str]: A dictionary containing extracted product information.
    """
    data = {}
    soup = bs(html, 'html.parser')

    # Extract the price value
    price_element = soup.select_one('.product-price_productPrice__YKAe0 span')
    price = price_element.text if price_element else ''
    data['price'] = price

    # Extract the number of likes
    parent_div = soup.select_one('.p_productPage__top__image__like__vFT4M')
    likes_element = parent_div.select_one('.product-like-button_like__button__38sAi')
    likes = likes_element.text if likes_element else ''
    data['product_likes'] = likes

    # Find all <ul> elements with the specified class name
    ul_elements = soup.select('.product-description-list_descriptionList__list__FJb05')

    # Iterate over each <ul> element
    for ul_element in ul_elements:
        # Get all the child <li> elements within the current <ul> element
        li_elements = ul_element.select('li')

        # Iterate over each <li> element
        for li_element in li_elements:
            # Find the <span> elements within the <li> element
            span_elements = li_element.select('span')

            # Extract the text content from the <span> elements
            property_name = span_elements[0].text

            if len(span_elements) > 1:
                property_value = span_elements[1].text
            else:
                property_value = ""

            # Store the extracted data in the dictionary
            data[property_name] = property_value

    return data

# Using Selenium WebDriver to extract product description
def get_description(driver) -> Dict[str, str]:
    """
    Extracts product description and likes using Selenium WebDriver.

    Args:
    - driver: The Selenium WebDriver instance.

    Returns:
    - Dict[str, str]: A dictionary containing extracted product description and likes.
    """
    data = {}
    # Find the description <div> element
    description_div = driver.find_element(By.CLASS_NAME, "product-seller-description_sellerDescription__nBvLe")

    # Check if the "Read more" button exists
    read_more_button = description_div.find_elements(By.CLASS_NAME, "product-seller-description_sellerDescription__action__btn--readMore__DIKI6")

    # If the "Read more" button exists, click it
    if read_more_button:
        read_more_button[0].click()
        # Wait for the full description to load (if necessary)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "product-seller-description_sellerDescription__action__btn__FmD48")))

    # Retrieve the full description text
    description_text = description_div.find_element(By.TAG_NAME, "p").text

    parent_div = driver.find_element(By.CLASS_NAME, "p_productPage__top__image__like__vFT4M")

    # Extract the number of likes
    likes_element = parent_div.find_element(By.CSS_SELECTOR, ".product-like-button_like__button__38sAi")
    likes = likes_element.text

    data['product_likes'] = likes
    data['product_description'] = description_text

    return data
