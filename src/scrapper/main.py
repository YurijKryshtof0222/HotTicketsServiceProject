import logging
import time

import search_container
from selenium import webdriver
from selenium.webdriver import ActionChains
from src import db_controller

from src.scrapper.scrapper_controler import ScrapperController

log_filename = time.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s\nINFO:%(message)s ',
    level=logging.ERROR,
    filename=f"logs/errors/{log_filename}.log",
    filemode="w",
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(url='https://www.otpusk.ua/')
    action_chain = ActionChains(driver)

    db_controller_instance = db_controller.DbController("..\my_database.db")
    db_controller_instance.create_table()

    from_country_elements_list = search_container.retrieve_from_countries_items(driver=driver, action_chain=action_chain)
    to_country_elements_list = search_container.retrieve_to_countries_items(driver=driver, action_chain=action_chain)
    duration_elements_list = search_container.retrieve_duration_items(driver=driver, action_chain=action_chain)

    driver.close()
    driver.quit()

    max_threads = 4

    scrapper = ScrapperController(from_country_elements_list[10:],
                                  to_country_elements_list,
                                  duration_elements_list[:5],
                                  db_controller_instance,
                                  max_threads)

    scrapper.traverse(limit=20, time_sleep=5)
