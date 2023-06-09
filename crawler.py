import os
import time
import urllib.request

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def crawl(search: str, dir_name: str, pause_time: int = 1):
    """
    Crawl images from Google image search
    :param search: keyword to search
    :param dir_name: directory name to save images
    :param pause_time: time to wait for page to load
    """

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        driver.get("https://www.google.com/search?q={}&tbm=isch&source=hp&sclient=img".format(search))

        os.makedirs(dir_name, exist_ok=True)

        last_height = driver.execute_script('return document.body.scrollHeight')
        while True:
            # Scroll down to bottom
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            # Wait to load page
            time.sleep(pause_time)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                try:
                    driver.find_element(By.CSS_SELECTOR, '.mye4qd').click()
                except NoSuchElementException:
                    break
            last_height = new_height

        images = driver.find_elements(By.CSS_SELECTOR, '.rg_i.Q4LuWd')
        count = 1
        for image in images:
            try:
                image.click()
                time.sleep(pause_time)
                image_url = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div['
                    '2]/a/img').get_attribute(
                    'src')
                opener = urllib.request.build_opener()
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(image_url, '{}/{}.jpg'.format(dir_name, count))
                count = count + 1
            except NoSuchElementException:
                pass
    finally:
        driver.close()


if __name__ == '__main__':
    crawl('dog', 'dogs')
