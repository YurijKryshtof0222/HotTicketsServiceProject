from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import util

url = "https://www.otpusk.ua/"
driver = webdriver.Chrome()
action = ActionChains(driver)

from_country_id = 0
to_country_id = 0
days_id = 0



def read_travel_info(url):
    driver.get(url)
    util.wait_for_element_presence(driver, delay=10, by=By.CLASS_NAME, value='src-pages-Offer-styles__head')

    header = driver.find_element(By.CLASS_NAME, 'src-pages-Offer-styles__head')
    hotel_name = header.find_element(By.TAG_NAME, 'h1').text
    location_info = header.find_element(By.TAG_NAME, 'a').text

    hotel_offer_info_el = driver.find_element(By.CLASS_NAME, 'src-containers-hotel-Offer-styles__offerContainer')

    dates_info_el = (hotel_offer_info_el
                          .find_element(By.CLASS_NAME, 'src-containers-hotel-Offer-styles__titleDate')
                          .find_element(By.XPATH, '..'))

    test1_info_el = dates_info_el.find_element(By.TAG_NAME, 'strong')
    nights_count = (dates_info_el.find_element(By.TAG_NAME, 'div')
                                      .find_element(By.TAG_NAME, 'div'))

    dates_info_el = (hotel_offer_info_el
                     .find_element(By.CLASS_NAME, 'src-containers-hotel-Offer-styles__titleTourists')
                     .find_element(By.XPATH, '..'))
    tourists_count_info_el = dates_info_el.find_element(By.TAG_NAME, 'strong')

    hotel_description = [el.text for el in (driver.find_element(By.CLASS_NAME,'src-pages-Offer-styles__hotelInfo')
                                                  .find_elements(By.TAG_NAME, 'span'))]

    print(hotel_name,
          f'Location: {location_info}',
          f'Nights count: {nights_count.text}',
          f'Dates: {test1_info_el.text}',
          f'Tourists count: {tourists_count_info_el.text}',
          f'link: {url}',
          f'Description: {hotel_description[1]}',
          sep='\n')
    print()


try:
    driver.get(url=url)
    filter_element = driver.find_element(By.CLASS_NAME,
                                         'src-containers-search-OtpuskInlineSearchForm-styles__submit')
    find_button_element = filter_element.find_element(By.TAG_NAME, 'button')

    action.click(find_button_element).perform()

    select_from_country = driver.find_element(By.ID, f'downshift-0-item-{from_country_id}')
    action.click(select_from_country).perform()

    select_to_country = driver.find_element(By.ID, f'downshift-1-item-{from_country_id}')
    action.click(select_to_country).perform()

    select_to_country = driver.find_element(By.ID, f'downshift-2-item-{days_id}')
    action.click(select_to_country).click(find_button_element).perform()

    util.wait_for_element_presence(driver, 5, By.CLASS_NAME, 'src-components-result-Card-styles__root')
    # time.sleep(10)

    links = list(util.traverse_links(driver))

    for a in links:
        read_travel_info(a)
    # check_travel_info(links[0])

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
