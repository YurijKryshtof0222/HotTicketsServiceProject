import logging

import traverser

from selenium import webdriver
from selenium.webdriver import ActionChains

url = "https://www.otpusk.ua/"
driver = webdriver.Chrome()
action = ActionChains(driver)

try:
    driver.get(url=url)
    links = list(traverser.get_offer_links(driver=driver, action=action))

    for a in links:
        try:
            traverser.read_offer_info(driver, a)
        except Exception as ex:
            logging.error(f'Cannot parsing the proposal by link: {a}\n{ex}')
    # check_travel_info(links[0])

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()