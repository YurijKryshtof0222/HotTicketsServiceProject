import logging

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import util
import time
import date_converter
from src.offer import Offer

log_filename = time.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s\nINFO:%(message)s ',
                    level=logging.ERROR,
                    filename=f"logs/errors/{log_filename}.log",
                    filemode="w",
                    datefmt='%Y-%m-%d %H:%M:%S')


def retrieve_img_urls(driver):
    img_container = driver.find_element(By.CLASS_NAME, 'src-components-hotel-PhotosCarousel-styles__view')
    action_chain = ActionChains(driver)
    action_chain.click(img_container).perform()

    photo_gallery_el = driver.find_element(By.CLASS_NAME, 'src-components-hotel-VerticalPhotosGallery-styles__item')
    action_chain.click(photo_gallery_el).perform()

    button_el = driver.find_element(By.CLASS_NAME,
                                    'arrow_b9bbag-o_O-arrow__direction__right_174p6a9-o_O-arrow__size__medium_9f7hgo')

    for i in range(5):
        image_el = driver.find_element(By.CLASS_NAME, 'image_1swebtw-o_O-imageLoaded_zgbg08')
        yield image_el.get_attribute('src')

        action_chain.click(button_el).perform()


def get_offer_info(driver, url):
    driver.get(url)
    util.wait_for_element_presence(driver, delay=10, by=By.CLASS_NAME, value='src-pages-Offer-styles__head')

    offer_id = int((driver.find_element(By.CLASS_NAME, 'src-containers-hotel-Offer-styles__offerCode')
                    .text.split(':')[-1]
                    .replace(' ', '')))

    header = driver.find_element(By.CLASS_NAME, 'src-pages-Offer-styles__head')
    offer_name = header.find_element(By.TAG_NAME, 'h1').text
    location_info = header.find_element(By.TAG_NAME, 'a').text

    hotel_offer_info_el = driver.find_element(By.CLASS_NAME, 'src-containers-hotel-Offer-styles__offerContainer')

    date_title_el = util.find_parent_element_of_child(
        hotel_offer_info_el, 'src-containers-hotel-Offer-styles__titleDate')
    date_interval_info_el = date_title_el.find_element(By.TAG_NAME, 'strong')

    date_interval_tuple = date_converter.convert_do_date(date_interval_info_el.text)
    start_date = date_interval_tuple[0]
    end_date = date_interval_tuple[1]

    nights_count_el = (date_title_el.find_element(By.TAG_NAME, 'div')
                       .find_element(By.TAG_NAME, 'div'))
    nights_count = int(''.join(filter(str.isdigit, nights_count_el.text)))

    title_people_el = util.find_parent_element_of_child(
        hotel_offer_info_el, 'src-containers-hotel-Offer-styles__titleTourists')
    people_count_info_el = title_people_el.find_element(By.TAG_NAME, 'strong')
    people_count = int(''.join(filter(str.isdigit, people_count_info_el.text)))

    food_title_el = util.find_parent_element_of_child(
        hotel_offer_info_el, 'src-containers-hotel-Offer-styles__titleRoomFood')
    food_info = food_title_el.find_elements(By.TAG_NAME, 'strong')[1].text

    transport_title_el = util.find_parent_element_of_child(
        hotel_offer_info_el, 'src-containers-hotel-Offer-styles__titleTransport')
    transport_from_info = transport_title_el.find_element(By.TAG_NAME, 'strong').text

    hotel_description = [el.text for el in (driver.find_element(By.CLASS_NAME, 'src-pages-Offer-styles__hotelInfo')
                                            .find_elements(By.TAG_NAME, 'span'))]

    price_info = int(hotel_offer_info_el.find_element(By.CLASS_NAME, 'src-containers-hotel-Offer-styles__priceBlock')
                     .find_element(By.TAG_NAME, 'nobr')
                     .text.split(' грн')[0]
                     .replace(' ', ''))

    images = list(retrieve_img_urls(driver=driver))

    return Offer(offer_id=offer_id,
                 name=offer_name,
                 source=url,
                 location=location_info,
                 people_count=people_count,
                 description=hotel_description[1],
                 food_info=food_info,
                 night_count=nights_count,
                 start_date=start_date,
                 end_date=end_date,
                 transport_info=transport_from_info,
                 price=price_info,
                 img_links=images)


def scrape_offer_from_url(driver, url, db, log_to_console: bool = True):
    offer = get_offer_info(driver, url)

    if log_to_console:
        offer.print_info()
        print()

    # offer.add_to_db(db)
    db.add_offer(offer)


def get_offer_links(driver,
                    action_chain,
                    from_country_item,
                    to_country_item,
                    duration_item,
                    limit):
    search_container_element = driver.find_element(By.ID, 'otp_search_form')
    downshift_element = search_container_element.find_element(By.CLASS_NAME, 'src-components-ui-Autocomplete'
                                                                             '-styles__input')
    action_chain.click(downshift_element).perform()

    util.wait_for_then_click(driver, 5, By.ID, from_country_item, action_chain)
    util.wait_for_then_click(driver, 5, By.ID, to_country_item, action_chain)

    select_duration = driver.find_element(By.ID, duration_item)
    filter_element = driver.find_element(By.CLASS_NAME,
                                         'src-containers-search-OtpuskInlineSearchForm-styles__submit')
    find_button_element = filter_element.find_element(By.TAG_NAME, 'button')
    action_chain.click(select_duration).click(find_button_element).perform()

    time.sleep(4)
    no_results_msg_element = driver.find_elements(By.CLASS_NAME, 'src-components-result'
                                                         '-SearchNothingFound-styles__root')
    if no_results_msg_element:
        return set()

    time.sleep(4)
    no_results_msg_element = driver.find_elements(By.CLASS_NAME, 'src-components-result'
                                                                 '-SearchNothingFound-styles__root')
    if no_results_msg_element:
        return set()

    time.sleep(4)
    no_results_msg_element = driver.find_elements(By.CLASS_NAME, 'src-components-result'
                                                                 '-SearchNothingFound-styles__root')
    if no_results_msg_element:
        return set()

    return util.present_links(driver, By.CLASS_NAME, 'src-containers-search-OtpuskSearchPageTemplate'
                                                     '-styles__resultsWrapper', limit=limit)
