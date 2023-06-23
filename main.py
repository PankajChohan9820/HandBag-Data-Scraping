#Import Libraries
from get_links import product_links
from helpers import helper
from helpers.handbag_info import get_description, general_information
from helpers.seller_info import seller_information
from helpers.image_download import download_seller_img, download_images

from re import findall
from os import path, makedirs
import shutil
from datetime import date
import pandas as pd
import warnings, logging
warnings.filterwarnings("ignore")



def get_basic_info(product_links,root_path, driver, logger):

    product_info_list = []
    for product_url in product_links:
        product_info = {}
        product_id = findall('[0-9]+', product_url)[-1]
        product_info["Reference"] = product_id
        product_folder = (root_path+'Data/{}'.format(product_id))

        # Create folder if it does not exist
        if not path.isdir(product_folder):
            makedirs(product_folder)
            logger.info("created folder : %s", product_folder)

        ## download images

        # Get product information
        driver.get(product_url)
        html=driver.page_source
        info = general_information(html)
        description = get_description(driver)
        seller_info = seller_information(driver)
        product_info.update(info)
        product_info.update(description)
        product_info.update(seller_info)
        download_seller_img(product_folder,product_id,driver, logger)
        download_images(product_id,root_path,logger)
        product_info_list.append(product_info)
    
    return product_info_list
    
    


if __name__=='__main__':
    try:
        #destination path where all your data will be
        root_path=r'G:/My Drive/Alex Yao/!!!!Research/!!!!Research projects/Ying Second hand luxury market/Data/data collection 20220518/'
        log_path = root_path+r'LogFile_{}.log'.format(date.today().strftime("%m-%d-%y"))
        logger = helper.get_logging(root_path, log_path)
        
        product_links = product_links()
        # product_links=product_links[60:72]

        #Seleninum custom driver
        driver = helper.get_webdriver()
        helper.handle_cookie(product_links[0],driver,logger)

        product_info_lists = get_basic_info(product_links,root_path, driver, logger)
        
        # convert list to dataframe and save to csv
        df = pd.DataFrame(product_info_lists)
        df.set_index('Reference', inplace=True)
        df.to_csv(root_path+r'Data\product_info_{}.csv'.format(date.today().strftime("%m%d%y")))
        
        logging.info('CODE EXECUTED SUCCESSFULLY')
        logging.shutdown()
        
        #Rename the folder name with the current date
        source=root_path+r'Data'
        des =root_path+r'Data_{}'.format(date.today().strftime("%m-%d-%y"))
        shutil.move(log_path,source)
        shutil.move(source,des)
    
    except Exception as e:
        print('Error message: ', str(e))


    
     


