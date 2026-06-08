from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
from common.setting import settings
from common.driver import create_driver

# @dataclass(frozen=True)
class Baseclass:
    def __init__(self, driver):
        self.driver = driver
    # driver : create_driver()

    # #获取网址
    # def get_url(self,url):
    #     self.driver.get(url)
    #
    # #关闭浏览器
    # def quit_browser(self):
    #     self.driver.quit()

    # #输入文本
    # def send_keys(self,selector,context):
    #     # self.driver.find_element(*selector).click()
    #     self.driver.find_element(*selector).send_keys(context)

    def wait_invisible(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_visible(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        wait = WebDriverWait(self.driver, timeout or settings.explicit_wait_seconds)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        wait = WebDriverWait(self.driver, timeout or settings.explicit_wait_seconds)
        return wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: tuple[str, str], timeout: int | None = None) -> None:
        self.wait_clickable(locator, timeout=timeout).click()

    def text_of(self, locator: tuple[str, str], timeout: int | None = None) -> str:
        return self.wait_visible(locator, timeout=timeout).text

    def is_visible(self, locator: tuple[str, str], timeout: int = 2) -> bool:
        try:
            self.wait_visible(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False