from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager  # This helps resolve the compatibility issue of Chrome version and WebDriver version
from fake_useragent import UserAgent
from datetime import date
import logging
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

def get_webdriver() -> webdriver.Chrome:
    """
    Initialize and configure a Chrome WebDriver instance.

    Returns:
    - webdriver.Chrome: The configured Chrome WebDriver instance.
    """
    ua = UserAgent()
    ua.update()
    ua.random
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

def get_logging(root_path: str, log_path: str) -> logging.Logger:
    """
    Initialize and configure a logging instance.

    Args:
    - root_path (str): Root path for data storage.
    - log_path (str): Path for the log file.

    Returns:
    - logging.Logger: The configured logging instance.
    """
    logging.basicConfig(filename=log_path, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('LogFile')
    logger.setLevel(logging.DEBUG)
    return logger

def handle_cookie(first_url: str, driver: webdriver.Chrome, logger: logging.Logger) -> None:
    """
    Handle website cookie pop-up by accepting it.

    Args:
    - first_url (str): The URL of the webpage with a cookie pop-up.
    - driver (webdriver.Chrome): The Chrome WebDriver instance.
    - logger (logging.Logger): The logging instance for log messages.

    Returns:
    - None
    """
    driver.get(first_url)
    timeout = 10
    # Handle cookie pop-up
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "tc-privacy-wrapper")))
        pop = driver.find_element(By.ID, "popin_tc_privacy_container_button")
        agree = pop.find_element(By.ID, "popin_tc_privacy_button_3")
        webdriver.ActionChains(driver).move_to_element(agree).click(agree).perform()
        logger.info("Passed cookie pop-up")
    except TimeoutException as e:
        logger.error("TimeoutException in handle_cookie as %s", str(e))
