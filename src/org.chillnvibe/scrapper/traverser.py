import logging
import util
import time

from selenium.webdriver.common.by import By

log_filename = time.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s\nINFO:%(message)s ',
                    level=logging.ERROR,
                    filename=f"logs/errors/{log_filename}.log",
                    filemode="w",
                    datefmt='%Y-%m-%d %H:%M:%S')

def read_offer_info(driver, url):
    driver.get(url)
    util.wait_for_element_presence(driver, delay=10, by=By.CLASS_NAME, value='src-pages-Offer-styles__head')

    offer_id = (driver.find_element(By.CLASS_NAME, 'src-containers-hotel-Offer-styles__offerCode')
                .text.split(':')[-1]
                .replace(' ', ''))

    header = driver.find_element(By.CLASS_NAME, 'src-pages-Offer-styles__head')
    hotel_name = header.find_element(By.TAG_NAME, 'h1').text
    location_info = header.find_element(By.TAG_NAME, 'a').text

    hotel_offer_info_el = driver.find_element(By.CLASS_NAME, 'src-containers-hotel-Offer-styles__offerContainer')

    date_title_el = util.find_parent_element_of_child(
        hotel_offer_info_el, 'src-containers-hotel-Offer-styles__titleDate')
    date_interval_info_el = date_title_el.find_element(By.TAG_NAME, 'strong')
    nights_count = (date_title_el.find_element(By.TAG_NAME, 'div')
                                 .find_element(By.TAG_NAME, 'div'))

    title_tourists_el = util.find_parent_element_of_child(
        hotel_offer_info_el, 'src-containers-hotel-Offer-styles__titleTourists')
    tourists_count_info_el = title_tourists_el.find_element(By.TAG_NAME, 'strong')

    food_title_el = util.find_parent_element_of_child(
        hotel_offer_info_el, 'src-containers-hotel-Offer-styles__titleRoomFood')
    food_info = food_title_el.find_elements(By.TAG_NAME, 'strong')[1]

    hotel_description = [el.text for el in (driver.find_element(By.CLASS_NAME, 'src-pages-Offer-styles__hotelInfo')
                                            .find_elements(By.TAG_NAME, 'span'))]

    print(f'Offer ID: {offer_id}',

          f'Offer name: {hotel_name}',
          f'Location: {location_info}',

          f'Nights count: {nights_count.text}',
          f'Dates: {date_interval_info_el.text}',

          f'Tourists count: {tourists_count_info_el.text}',
          f'Food_info: {food_info.text}',

          f'link: {url}',
          f'Description: {hotel_description[1]}',

          sep='\n')
    print()


def get_offer_links(driver, action, from_country_id= 0, to_country_id= 0, days_id= 0):
    filter_element = driver.find_element(By.CLASS_NAME,
                                         'src-containers-search-OtpuskInlineSearchForm-styles__submit')
    find_button_element = filter_element.find_element(By.TAG_NAME, 'button')

    action.click(find_button_element).perform()

    select_from_country = driver.find_element(By.ID, f'downshift-0-item-{from_country_id}')
    action.click(select_from_country).perform()

    select_to_country = driver.find_element(By.ID, f'downshift-1-item-{to_country_id}')
    action.click(select_to_country).perform()

    select_to_country = driver.find_element(By.ID, f'downshift-2-item-{days_id}')
    action.click(select_to_country).click(find_button_element).perform()

    util.wait_for_element_presence(driver, 15, By.CLASS_NAME, 'src-components-result-Card-styles__root')

    return util.present_links(driver, By.CLASS_NAME, 'src-containers-search-OtpuskSearchPageTemplate'
                                                     '-styles__resultsWrapper')
