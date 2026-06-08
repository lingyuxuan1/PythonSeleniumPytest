from __future__ import annotations

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
from common.setting import settings
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions


def _chrome() -> webdriver.Chrome:
    #options = ChromeOptions()
    # if settings.headless:
    #     options.add_argument("--headless=new")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1280,900")
    return webdriver.Chrome()


def _edge() -> webdriver.Edge:
    options = EdgeOptions()
    options.add_experimental_option("detach", True)  # 保持浏览器不关闭
    # 指定你下载的驱动路径
    service = Service(executable_path=r"D:\down\edgedriver_win64 (1)\msedgedriver.exe")
    return webdriver.Edge(service=service, options=options)

def _firefox() -> webdriver.Firefox:
    # options = FirefoxOptions()
    # if settings.headless:
    #     options.add_argument("-headless")
    return webdriver.Firefox()


def create_driver():
    """
    Create a Selenium WebDriver.

    Notes:
    - Relies on Selenium Manager (Selenium 4.6+) to locate browser drivers automatically.
    - Use env `BROWSER` and `HEADLESS` to switch behavior.
    """
    browser = settings.browser
    if browser == "chrome":
        driver = _chrome()
    elif browser == "edge":
        driver = _edge()
    elif browser == "firefox":
        driver = _firefox()
    else:
        raise ValueError(f"Unsupported BROWSER={browser!r}. Use chrome/edge/firefox.")

    driver.implicitly_wait(settings.implicit_wait_seconds)
    driver.set_page_load_timeout(settings.page_load_timeout_seconds)
    return driver

