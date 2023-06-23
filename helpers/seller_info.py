
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

def seller_information(driver):
    try:
        data ={}
        parent_div = driver.find_element(By.CLASS_NAME, "product-seller-block_sellerBlock__details__50J7I")

        # Find the <a> element containing the seller URL
        seller_link = parent_div.find_element(By.CSS_SELECTOR, "a[href*='members/profile']")

        # Extract the seller URL
        seller_url = seller_link.get_attribute("href")

        driver.get(seller_url)
        # Assuming you have obtained the HTML content of the seller's profile page and stored it in the 'html' variable
        # Create a BeautifulSoup object to parse the HTML
        soup = bs(driver.page_source, 'html.parser')

        # Extract seller's name
        seller_name = soup.select_one('span[property="v:name"]').text.strip()

        # Extract seller's email id (if available)
        seller_email = soup.select_one('a[href^="mailto:"]').get('href')[7:] if soup.select_one('a[href^="mailto:"]') else None

        # Extract seller's total sold products and recent number of sold products
        seller_total_sold = soup.select_one('.history_sold strong').text.strip().split()[0]
        seller_recent_sold = soup.select_one('.recent_sold strong').text.strip().split()[0]

        # Extract seller's country
        seller_country = soup.select_one('.profile-infos li:first-child').text.strip()

        # Extract seller's join date
        seller_join_date = soup.select_one('.profile-infos li:last-child').text.strip().split(' ')[-3:]
        seller_badge = soup.find('span', class_='vc-badge__text')
        if seller_badge:
            badge_data = seller_badge.text.strip()
        else:
            badge_data = None
        
        data['seller_name']=seller_name
        data['item_sold_by_seller']=seller_total_sold
        data['seller_description']= {
            'email':seller_email,
            'seller_recent_sold':seller_recent_sold,
            'seller_total_sold':seller_total_sold,
            'country':seller_country,
            'join_date':seller_join_date,
        }
        data['seller_type']:badge_data
        
        return data

    except Exception as e:
        # print(str(e))
        return {}