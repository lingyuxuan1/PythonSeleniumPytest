from __future__ import annotations

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
from common.setting import settings
# Selenium 4.6+ 自带 Selenium Manager，不再需要 webdriver_manager 联网下载驱动


def _chrome() -> webdriver.Chrome:
    """创建 Chrome 浏览器驱动。"""
    #options = ChromeOptions()
    # if settings.headless:
    #     options.add_argument("--headless=new")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1280,900")
    return webdriver.Chrome()


def _edge() -> webdriver.Edge:
    """创建 Edge 浏览器驱动。

    Notes:
    - 依赖 Selenium Manager（Selenium 4.6+）自动下载/匹配 EdgeDriver，
      避免 webdriver_manager 联网拉取 LATEST_RELEASE 失败（azureedge.net 易被拦截）。
    - 如需固定驱动版本，可改用 Service(executable_path=...) 指定本地 msedgedriver。
    """
    options = webdriver.EdgeOptions()
    return webdriver.Edge(options=options)

def _firefox() -> webdriver.Firefox:
    """创建 Firefox 浏览器驱动。"""
    # options = FirefoxOptions()
    # if settings.headless:
    #     options.add_argument("-headless")
    return webdriver.Firefox()


def create_driver() -> webdriver.Remote:
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

