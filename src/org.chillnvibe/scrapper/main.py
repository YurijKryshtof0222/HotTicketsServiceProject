import logging
import time

import retriever

from selenium import webdriver
from selenium.webdriver import ActionChains

url = "https://www.otpusk.ua/"
driver = webdriver.Chrome()
action = ActionChains(driver)


def traverse_offer_links_from_search_container(from_country_item, to_country_item, days_item):
    # driver.get(url=url)
    # time.sleep(5)
    links = list(retriever.get_offer_links(
            driver=driver,
            action_chain=ActionChains(driver),
            from_country_item=from_country_item,
            to_country_item=to_country_item,
            duration_item=days_item))
    for a in links:
        try:
            retriever.read_offer_info(driver, a)
        except Exception as ex:
            logging.error(f'Cannot parsing the proposal by link: {a}\n{ex}')


if __name__ == '__main__':
    driver.get(url=url)
    from_country_elements_list = retriever.retrieve_from_countries_elements(driver=driver, action_chain=action)
    to_country_elements_list = retriever.retrieve_to_countries_elements(driver=driver, action_chain=action)
    duration_elements_list = retriever.retrieve_duration_elements(driver=driver, action_chain=action)

    for from_country in from_country_elements_list:
        for to_country in to_country_elements_list:
            for duration in duration_elements_list:
                traverse_offer_links_from_search_container(from_country, to_country, duration)