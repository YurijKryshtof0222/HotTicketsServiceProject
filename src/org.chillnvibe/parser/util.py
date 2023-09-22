from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def traverse_links(driver):
    href_list = (driver.find_element(By.CLASS_NAME, 'src-containers-search-OtpuskSearchPageTemplate-styles__resultsWrapper')
                       .find_elements(By.TAG_NAME, 'a'))
    return (a.get_attribute('href') for a in href_list if a.get_attribute('href'))


def wait_for_element_presence(driver, delay, by, value):
    WebDriverWait(driver, delay).until(
        expected_conditions.presence_of_element_located((by, value)))