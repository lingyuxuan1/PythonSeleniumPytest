from time import sleep

from selenium import webdriver
import pytest
from common.com import *
from common.driver import *
from common.setting import settings
from page.login_page import LoginPage


LOGIN_USERNAME = "17774816826"
LOGIN_PASSWORD = "12345678A"


@pytest.fixture(scope="function")
def driver():
    print("打开浏览器")
    driver = create_driver()
    driver.get(settings.base_url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def login_driver(driver):
    login_page = LoginPage(driver)
    login_result = login_page.do_login(LOGIN_USERNAME, LOGIN_PASSWORD)
    assert login_result == "我的", "登录失败，未进入系统首页"
    return driver
