from os import path, makedirs, listdir,fsync
from re import sub
from selenium.webdriver.common.by import By
import cloudscraper
scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    })


def download_seller_img(image_folder,product_id,driver, logger):
    try:
        
        img_element = driver.find_element(By.ID, 'profil_img')

        # Get the value of the "src" attribute of the img element
        image_url = img_element.get_attribute('src')
        
        # Replace width and height with 500x500
        modified_url = sub(r'w=\d+', 'w=500', image_url)
        image_url = sub(r'h=\d+', 'h=500', modified_url)
        
        logger.info("Img of seller of %s : %s",str(product_id),str(image_url.split("/")[-1]))
    
        filename= 'sellerImg_'+str(product_id) + '_'+image_url.split("/")[-1]
        file_path = path.join(image_folder, filename)
        r = scraper.get(image_url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(file_path,'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        fsync(f.fileno())
            # print('Seller image sucessfully Downloaded: ',filename)
            logger.info('Seller image sucessfully Downloaded: %s',filename)
        else:
            logger.debug('Seller image not sucessfully Donwnloaded')
    except Exception as e:
        # print(str(e))
        logger.error("Error at download_seller_img function %s",str(e))


def download_images(product_id, root_path, logger):
    try:
        image_folder = root_path+'Data/{}/Images'.format(product_id)
        if not path.exists(image_folder):
            makedirs(image_folder)
            image_count = 0
        else:
            image_count = len(listdir(image_folder))

        for i in range(image_count+1,30):
            image_url = "https://images.vestiairecollective.com/cdn-cgi/image/w=500,h=500,q=80,f=auto,/produit/{}-{}_1.jpg".format(product_id, i)
            filename = image_url.split("/")[-1]
            file_path = path.join(image_folder, filename)
            r = scraper.get(image_url, stream=True)
            if r.status_code == 200:
                r.raw.decode_content = True
                with open(file_path,'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 8):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            fsync(f.fileno())
                # print('Image sucessfully Downloaded: ',filename)
                # logger.info('Image sucessfully Downloaded: %s',filename)
                image_count += 1
            else:
                break
        return image_count
    except Exception as e:
        # print(str(e))
        return
        # logger.error('Error at download_images function: %s',str(e))

