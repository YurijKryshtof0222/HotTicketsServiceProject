import logging
import time
from concurrent.futures import ThreadPoolExecutor

from src.scrapper import search_container


def traverse_links_thread(db_controller_instance, from_country, to_country, duration, limit):
    try:
        search_container.traverse_offer_links(from_country, to_country, duration, db_controller_instance, limit=limit)
    except Exception as ex:
        logging.error(f'Cannot traverse links from these choice combination:\n{ex}')


class ScrapperController:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not ScrapperController.__instance:
            ScrapperController.__instance = super().__new__(cls)
        return ScrapperController.__instance

    def __init__(self,
                 from_country_elements_list,
                 to_country_elements_list,
                 duration_elements_list,
                 db_controller_instance,
                 max_threads):
        self.__from_country_elements_list = from_country_elements_list
        self.__to_country_elements_list = to_country_elements_list
        self.__duration_elements_list = duration_elements_list
        self.__db_controller_instance = db_controller_instance
        self.__max_threads = max_threads

    def traverse(self, limit=20, time_sleep=5):
        with ThreadPoolExecutor(self.__max_threads) as executor:
            for from_country in self.__from_country_elements_list:
                for to_country in self.__to_country_elements_list:
                    for duration in self.__duration_elements_list[:3]:
                        # Submit tasks to the thread pool
                        executor.submit(self.__db_controller_instance,
                                        traverse_links_thread,
                                        from_country,
                                        to_country,
                                        duration,
                                        limit)
                        time.sleep(time_sleep)
