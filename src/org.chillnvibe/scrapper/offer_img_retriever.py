from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

root_url = "https://www.otpusk.ua/"


def retrieve_img_urls(driver):
    img_container = driver.find_element(By.CLASS_NAME, 'src-components-hotel-PhotosCarousel-styles__view')
    action_chain = ActionChains(driver)
    action_chain.click(img_container).perform()

    photo_gallery_el = driver.find_element(By.CLASS_NAME, 'src-components-hotel-VerticalPhotosGallery-styles__item')
    action_chain.click(photo_gallery_el).perform()

    button_el = driver.find_element(By.CLASS_NAME, 'arrow_b9bbag-o_O-arrow__direction__right_174p6a9-o_O-arrow__size__medium_9f7hgo')

    for i in range(5):
        image_el = driver.find_element(By.CLASS_NAME, 'image_1swebtw-o_O-imageLoaded_zgbg08')
        yield image_el.get_attribute('src')

        action_chain.click(button_el).perform()
