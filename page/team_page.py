import random

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from common.com import Baseclass
from common.setting import settings


class TeamPage(Baseclass):
    team_path = "/team"

    create_my_team_button = (
        "xpath",
        "//div[contains(@class,'w-16')"
        " and contains(@class,'h-16')"
        " and contains(@class,'bg-blue-50')"
        " and contains(@class,'text-blue-600')"
        " and .//*[contains(@class,'lucide-plus')]]",
    )
    create_official_team_button = (
        "xpath",
        "//*[normalize-space()='创建官方团队']"
        "/ancestor::*[contains(@class,'group') or contains(@class,'cursor-pointer')][1]"
        " | //*[self::button or @role='button'][contains(normalize-space(),'创建官方团队')]",
    )
    ai_avatar_button = (
        "xpath",
        "//button[contains(normalize-space(),'AI生成头像')]",
    )
    ai_avatar_style_input = (
        "xpath",
        "//input[@placeholder='输入生成风格，如：极简 靛蓝色 线条感...']",
    )
    ai_avatar_generate_button = (
        "xpath",
        "(//button[contains(normalize-space(),'生成')"
        " or contains(normalize-space(),'确认')"
        " or contains(normalize-space(),'确定')][not(contains(normalize-space(),'AI生成头像'))])[last()]",
    )
    complete_create_button = (
        "xpath",
        "//button[contains(normalize-space(),'完成创建')]",
    )
    create_team_dialog = (
        "xpath",
        "(//*[contains(@class,'arco-modal') or contains(@class,'arco-drawer')][.//button[contains(normalize-space(),'完成创建')]])[last()]",
    )
    team_name_input = (
        "xpath",
        "(//input[@placeholder='例如：销售团队'"
        " or contains(@placeholder,'团队名称')"
        " or contains(@placeholder,'团队名')"
        " or ancestor::*[contains(normalize-space(),'团队名称')]][not(@disabled)])[last()]",
    )
    team_description_input = (
        "xpath",
        "(//*[self::textarea or self::input]"
        "[contains(@placeholder,'团队描述')"
        " or contains(@placeholder,'团队介绍')"
        " or contains(@placeholder,'团队简介')"
        " or ancestor::*[contains(normalize-space(),'团队描述')"
        " or contains(normalize-space(),'团队介绍')"
        " or contains(normalize-space(),'团队简介')]][not(@disabled)])[last()]",
    )
    success_message = (
        "xpath",
        "//*[contains(@class,'arco-message') or contains(@class,'arco-notification')]"
        "//*[contains(normalize-space(),'创建成功') or contains(normalize-space(),'成功')]",
    )
    team_sidebar_list = (
        "xpath",
        "(//*[.//*[normalize-space()='易法通AI']"
        " and .//*[normalize-space()='对话助手']"
        " and not(ancestor::*[contains(@class,'arco-modal')"
        " or contains(@class,'arco-drawer')])])[last()]",
    )

    # 进入团队页。
    def open_team_page(self) -> None:
        self.driver.get(f"{settings.base_url.rstrip('/')}{self.team_path}")
        self.wait_visible(self.create_my_team_button, timeout=20)

    # 打开创建团队弹窗或表单。
    def open_create_team_panel(self, official: bool = False) -> None:
        create_button = self.create_official_team_button if official else self.create_my_team_button
        self.click(create_button, timeout=20)
        self.wait_visible(self.complete_create_button, timeout=20)

    # 点击 AI 生成头像，随机输入风格后点击生成。
    def generate_ai_avatar(self) -> None:
        self.click(self.ai_avatar_button, timeout=20)
        style = random.choice(
            [
                "极简 靛蓝色 线条感",
                "科技感 蓝紫渐变",
                "扁平化 明亮 专业",
                "商务风 简洁 圆形图标",
            ]
        )
        style_input = self.wait_visible(self.ai_avatar_style_input, timeout=20)
        self._fill_field(style_input, style)
        self.click(self.ai_avatar_generate_button, timeout=20)
        self.wait_ai_avatar_generation_finished()

    # 等待 AI 头像生成完成，兼容生成后弹窗关闭或按钮恢复可用两种表现。
    def wait_ai_avatar_generation_finished(self, timeout: int = 30) -> bool:
        def generation_finished(driver: WebDriver) -> bool:
            try:
                visible_style_inputs = [
                    element
                    for element in driver.find_elements(*self.ai_avatar_style_input)
                    if element.is_displayed()
                ]
                if not visible_style_inputs:
                    return True

                buttons = [
                    element
                    for element in driver.find_elements(*self.ai_avatar_generate_button)
                    if element.is_displayed()
                ]
                return bool(buttons) and buttons[-1].is_enabled()
            except StaleElementReferenceException:
                return False

        try:
            WebDriverWait(self.driver, timeout).until(
                generation_finished,
                message="AI头像生成未完成",
            )
            return True
        except TimeoutException:
            return False

    # 构造可安全放入 XPath 表达式的文本字面量。
    def _xpath_literal(self, value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    # 获取当前创建团队表单根节点，优先使用弹窗/抽屉。
    def _create_team_root(self) -> WebDriver | WebElement:
        for root in self.driver.find_elements(*self.create_team_dialog):
            if root.is_displayed():
                return root
        return self.driver

    # 获取创建团队表单中可输入的字段，作为页面字段文案变化时的兜底。
    def _visible_enabled_fields(self) -> list[WebElement]:
        root = self._create_team_root()
        fields = root.find_elements(
            By.XPATH,
            ".//*[self::input or self::textarea]"
            "[not(@disabled) and not(@readonly)"
            " and not(@type='hidden')"
            " and not(@type='checkbox')"
            " and not(@type='radio')]",
        )
        return [field for field in fields if field.is_displayed()]

    # 输入文本前清空字段，兼容部分前端组件 clear 不生效。
    def _fill_field(self, field: WebElement, value: str) -> None:
        field.click()
        field.clear()
        if field.get_attribute("value"):
            self.driver.execute_script("arguments[0].value = '';", field)
        field.send_keys(value)

    # 填写团队名称。
    def fill_team_name(self, team_name: str) -> None:
        try:
            name_input = self.wait_visible(self.team_name_input, timeout=8)
        except TimeoutException:
            fields = self._visible_enabled_fields()
            if not fields:
                raise AssertionError("未找到团队名称输入框")
            name_input = fields[0]
        self._fill_field(name_input, team_name)

    # 填写团队描述，若页面没有该字段则跳过。
    def fill_team_description(self, description: str) -> None:
        try:
            description_input = self.wait_visible(self.team_description_input, timeout=4)
        except TimeoutException:
            fields = self._visible_enabled_fields()
            if len(fields) < 2:
                return
            description_input = fields[1]
        self._fill_field(description_input, description)

    # 点击完成创建并等待弹窗关闭或成功提示出现。
    def submit_create_team(self) -> bool:
        self.click(self.complete_create_button, timeout=20)

        def create_finished(driver: WebDriver) -> bool:
            if self.is_visible(self.success_message, timeout=1):
                return True
            try:
                return not any(
                    element.is_displayed()
                    for element in driver.find_elements(*self.create_team_dialog)
                )
            except StaleElementReferenceException:
                return False

        try:
            WebDriverWait(self.driver, 20).until(
                create_finished,
                message="点击完成创建后未看到创建成功结果",
            )
            return True
        except TimeoutException:
            return False

    # 完整创建团队流程。
    def create_team(self, team_name: str, description: str) -> bool:
        self.open_create_team_panel()
        self.generate_ai_avatar()
        self.fill_team_name(team_name)
        self.fill_team_description(description)
        return self.submit_create_team()

    # 完整创建官方团队流程。
    def create_official_team(self, team_name: str, description: str) -> bool:
        self.open_create_team_panel(official=True)
        self.generate_ai_avatar()
        self.fill_team_name(team_name)
        self.fill_team_description(description)
        return self.submit_create_team()

    # 判断左侧团队列表中是否可见指定团队名称。
    def is_team_visible(self, team_name: str, timeout: int = 20) -> bool:
        team_literal = self._xpath_literal(team_name)

        def team_visible_in_sidebar(driver: WebDriver) -> bool:
            try:
                for sidebar in driver.find_elements(*self.team_sidebar_list):
                    if not sidebar.is_displayed():
                        continue

                    for _ in range(5):
                        teams = sidebar.find_elements(
                            By.XPATH,
                            f".//*[text()[contains(normalize-space(.), {team_literal})]]",
                        )
                        if any(team.is_displayed() for team in teams):
                            return True

                        driver.execute_script(
                            "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].clientHeight;",
                            sidebar,
                        )
            except StaleElementReferenceException:
                return False

            return False

        try:
            WebDriverWait(self.driver, timeout).until(
                team_visible_in_sidebar,
                message=f"左侧团队列表中未找到新创建的团队: {team_name}",
            )
            return True
        except TimeoutException:
            return False
