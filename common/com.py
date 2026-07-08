from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from common.setting import settings


class Baseclass:
    def __init__(self, driver: WebDriver) -> None:
        """初始化页面对象使用的浏览器驱动。"""
        self.driver = driver

    def wait_invisible(self, locator: tuple[str, str], timeout: int = 10) -> bool:
        """等待指定元素不可见。"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(
            EC.invisibility_of_element_located(locator),
            message=f"等待元素不可见超时: {locator}",
        )

    def wait_visible(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        """等待指定元素可见并返回该元素。"""
        wait = WebDriverWait(self.driver, timeout or settings.explicit_wait_seconds)
        return wait.until(
            EC.visibility_of_element_located(locator),
            message=f"等待元素可见超时: {locator}",
        )

    def wait_clickable(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        """等待指定元素可点击并返回该元素。"""
        wait = WebDriverWait(self.driver, timeout or settings.explicit_wait_seconds)
        return wait.until(
            EC.element_to_be_clickable(locator),
            message=f"等待元素可点击超时: {locator}",
        )

    def click(self, locator: tuple[str, str], timeout: int | None = None) -> None:
        """等待元素可点击后执行点击。"""
        self.wait_clickable(locator, timeout=timeout).click()

    def text_of(self, locator: tuple[str, str], timeout: int | None = None) -> str:
        """获取指定可见元素的文本。"""
        return self.wait_visible(locator, timeout=timeout).text

    def is_visible(self, locator: tuple[str, str], timeout: int = 2) -> bool:
        """判断指定元素在超时时间内是否可见。"""
        try:
            self.wait_visible(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False
