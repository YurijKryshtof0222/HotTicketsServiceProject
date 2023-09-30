import logging

from selenium.webdriver import ActionChains
from selenium import webdriver

import util
import retriever

from selenium.webdriver.common.by import By


def traverse_offer_links(from_country_item, to_country_item, days_item):
    temp_driver = webdriver.Chrome()
    temp_driver.get(url='https://www.otpusk.ua/')
    temp_action_chain = ActionChains(temp_driver)
    try:
        links = list(retriever.get_offer_links(
            driver=temp_driver,
            action_chain=temp_action_chain,
            from_country_item=from_country_item,
            to_country_item=to_country_item,
            duration_item=days_item))
        for a in links:
            try:
                retriever.get_offer_info(temp_driver, a)
            except Exception as ex:
                logging.error(f'Cannot parsing the proposal by link: {a}\n{ex}')
    finally:
        temp_driver.close()
        temp_driver.quit()


def retrieve_items_from_search_container_by_id(driver, action_chain, by, value):
    util.wait_for_element_presence(driver, delay=10, by=By.ID,
                                   value='otp_search_form')
    search_container_element = driver.find_element(By.ID,
                                         'otp_search_form')
    downshift_element = search_container_element.find_element(by, value)
    action_chain.click(downshift_element).perform()

    return [a.get_attribute('id') for a in search_container_element.find_elements(By.TAG_NAME, 'li')]


def retrieve_from_countries_items(driver, action_chain):
    return retrieve_items_from_search_container_by_id(driver, action_chain, By.ID, 'downshift-0-input')


def retrieve_to_countries_items(driver, action_chain):
    return retrieve_items_from_search_container_by_id(driver, action_chain, By.ID, 'downshift-1-input')


def retrieve_duration_items(driver, action_chain):
    return retrieve_items_from_search_container_by_id(driver, action_chain, By.CLASS_NAME, 'durationControlRoot')