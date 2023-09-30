import logging
import time

import retriever
import search_container

from selenium import webdriver
from selenium.webdriver import ActionChains

log_filename = time.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s\nINFO:%(message)s ',
                    level=logging.ERROR,
                    filename=f"logs/errors/{log_filename}.log",
                    filemode="w",
                    datefmt='%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(url='https://www.otpusk.ua/')
    action_chain = ActionChains(driver)

    from_country_elements_list = search_container.retrieve_from_countries_items(driver=driver, action_chain=action_chain)
    to_country_elements_list = search_container.retrieve_to_countries_items(driver=driver, action_chain=action_chain)
    duration_elements_list = search_container.retrieve_duration_items(driver=driver, action_chain=action_chain)

    driver.close()
    driver.quit()

    for from_country in from_country_elements_list:
        for to_country in to_country_elements_list:
            for duration in duration_elements_list:
                try:
                    search_container.traverse_offer_links(from_country, to_country, duration)
                except Exception as ex:
                    logging.error(f'Cannot traverse links from these choice combination:\n{ex}')