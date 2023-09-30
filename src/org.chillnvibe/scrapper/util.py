from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def present_links(driver, by, value, limit=0) -> set:
    href_list = (driver.find_element(by, value)
                       .find_elements(By.TAG_NAME, 'a'))
    links_set = set()
    for a in href_list:
        if limit != 0 and len(links_set) >= limit:
            break
        href = a.get_attribute('href')
        if href:
            links_set.add(href)
    return links_set
    # return {a.get_attribute('href') for a in href_list if len(links_set) >= limit and a.get_attribute('href')}


def wait_for_element_presence(driver, delay, by, value):
    WebDriverWait(driver, delay).until(
        expected_conditions.presence_of_element_located((by, value)))



def find_parent_element_of_child(enclosed_element, child_element, by=By.CLASS_NAME):
    return (enclosed_element.find_element(by, child_element)
                            .find_element(By.XPATH, '..'))