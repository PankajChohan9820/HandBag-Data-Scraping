
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager # this helps resolve the compatibability issue of chrome version and webdriver version 
from fake_useragent import UserAgent
from datetime import date
import logging
import warnings
warnings.filterwarnings("ignore")



def get_webdriver():
    ua = UserAgent()
    ua.update()
    ua.random
    headers={ "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.17 Safari/537.36",
            "x-nba-stats-origin": "stats"}

    user_agent = ua.random
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--headless")
    options.add_argument('window-size=1200x600')
    options.add_argument(f'user-agent={user_agent}') 
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options) 
    driver.maximize_window()
    driver.implicitly_wait(2)
    return driver


def get_logging(root_path, log_path):
    
    logging.basicConfig(filename=log_path, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('LogFile')
    logger.setLevel(logging.DEBUG)

    return logger

def handle_cookie(first_url,driver,logger):
    driver.get(first_url)
    timeout = 10
    # handle cookie pop out
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "tc-privacy-wrapper")))
        pop = driver.find_element(By.ID, "popin_tc_privacy_container_button")
        agree = pop.find_element(By.ID, "popin_tc_privacy_button_3")
        webdriver.ActionChains(driver).move_to_element(agree).click(agree).perform()
        # print("pass cookie pop-up")
        logger.info("pass cookie pop-up")
    except TimeoutException as e:
        logger.error("TimeoutException in handle_cookie as %s",str(e))

