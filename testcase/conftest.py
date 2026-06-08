from time import sleep

from selenium import webdriver
import pytest
from common.com import *
from common.driver import *
from common.setting import settings

@pytest.fixture(scope="function")
def driver():
    print("打开浏览器")
    driver = create_driver()
    driver.get(settings.base_url)
    driver.maximize_window()
    yield driver
    driver.quit()








