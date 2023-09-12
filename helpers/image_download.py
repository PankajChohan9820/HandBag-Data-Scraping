from os import path, makedirs, listdir, fsync
from re import sub
from selenium.webdriver.common.by import By
import cloudscraper
from cloudscraper import CloudScraper
from typing import Optional
import logging

# Initialize CloudScraper
scraper: CloudScraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    })

def download_seller_img(image_folder: str, product_id: str, driver: By, logger: logging.Logger) -> None:
    """
    Download the seller's image.

    Args:
    - image_folder (str): The folder where images will be saved.
    - product_id (str): The product ID.
    - driver (By): The Selenium WebDriver element locator.
    - logger (logging.Logger): The logging instance.

    Returns:
    - None
    """
    try:
        img_element = driver.find_element(By.ID, 'profil_img')

        # Get the value of the "src" attribute of the img element
        image_url = img_element.get_attribute('src')

        # Replace width and height with 500x500
        modified_url = sub(r'w=\d+', 'w=500', image_url)
        image_url = sub(r'h=\d+', 'h=500', modified_url)

        logger.info("Seller image of %s : %s", str(product_id), str(image_url.split("/")[-1]))

        filename = 'sellerImg_' + str(product_id) + '_' + image_url.split("/")[-1]
        file_path = path.join(image_folder, filename)
        r = scraper.get(image_url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        fsync(f.fileno())
            logger.info('Seller image successfully Downloaded: %s', filename)
        else:
            logger.debug('Seller image not successfully Downloaded')
    except Exception as e:
        logger.error("Error at download_seller_img function: %s", str(e))

def download_images(product_id: str, root_path: str, logger: logging.Logger) -> Optional[int]:
    """
    Download product images.

    Args:
    - product_id (str): The product ID.
    - root_path (str): Root path for data storage.
    - logger (logging.Logger): The logging instance.

    Returns:
    - Optional[int]: The number of images downloaded, or None in case of an error.
    """
    try:
        image_folder = path.join(root_path, 'Data', str(product_id), 'Images')
        if not path.exists(image_folder):
            makedirs(image_folder)
            image_count = 0
        else:
            image_count = len(listdir(image_folder))

        for i in range(image_count + 1, 30):
            image_url = "https://images.vestiairecollective.com/cdn-cgi/image/w=500,h=500,q=80,f=auto,/produit/{}-{}_1.jpg".format(product_id, i)
            filename = image_url.split("/")[-1]
            file_path = path.join(image_folder, filename)
            r = scraper.get(image_url, stream=True)
            if r.status_code == 200:
                r.raw.decode_content = True
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 8):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            fsync(f.fileno())
                image_count += 1
            else:
                break
        return image_count
    except Exception as e:
        logger.error('Error at download_images function: %s', str(e))
        return None
