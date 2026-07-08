from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from common.com import Baseclass
from common.setting import settings


class SkillPage(Baseclass):
    skills_path = "/skills"

    skill_menu = ("xpath", "//span[contains(@class,'menu-label') and normalize-space()='技能']")
    my_skills_tab = ("xpath", "//*[self::span or self::div or self::button][normalize-space()='我的技能']")
    my_created_tab = ("xpath", "//*[self::span or self::div or self::button][normalize-space()='我创建的']")
    skill_store_tab = ("xpath", "//*[self::span or self::div or self::button][normalize-space()='技能商店']")
    official_tab = ("xpath", "//*[self::span or self::div or self::button][normalize-space()='官方技能' or normalize-space()='官方']")
    all_tab = ("xpath", "//*[self::span or self::div or self::button][normalize-space()='全部技能' or normalize-space()='全部']")
    team_tab = ("xpath", "//*[self::span or self::div or self::button][normalize-space()='团队' or normalize-space()='团队技能']")
    conversation_tab = ("xpath", "//*[self::span or self::div or self::button][normalize-space()='对话']")
    ai_selector = ("xpath", "//div[text()='易法通AI']")
    chat_input_container = (
        "css selector",
        "div.flex.flex-wrap.gap-2.mb-2",
    )

    create_skill_button = ("xpath", "//button[contains(@class,'arco-btn') and contains(.,'创建技能')]")
    first_instruction_input = (
        "xpath",
        "//input[@placeholder='在此输入您的第一个指令，开启 AI 技能创作...']",
    )
    send_button = (
        "xpath",
        "//input[@placeholder='在此输入您的第一个指令，开启 AI 技能创作...']"
        "/following::div[contains(@class,'cursor-pointer') and .//*[contains(@class,'lucide-arrow-up')]][1]",
    )
    add_to_my_skills_button = ("xpath", "//button[normalize-space()='添加到我的技能']")
    confirm_add_button = ("xpath", "//button[normalize-space()='确认添加']")

    publish_to_store_button = (
        "xpath",
        "//button[contains(normalize-space(),'上架技能商店') or contains(normalize-space(),'上架到技能商店')]",
    )
    publish_to_team_button = ("xpath", "//button[contains(normalize-space(),'上架到团队')]")
    run_now_button = ("xpath", "//button[contains(normalize-space(),'即刻运行')]")
    confirm_publish_button = ("xpath", "//button[normalize-space()='确认上架']")
    team_publish_modal = (
        "xpath",
        "(//*[contains(@class,'arco-modal') and .//button[normalize-space()='确认上架']])[last()]",
    )
    first_team_in_publish_modal = (
        "xpath",
        "((//*[contains(@class,'arco-modal') and .//button[normalize-space()='确认上架']])[last()]"
        "//span[contains(@class,'text-[15px]')"
        " and contains(@class,'font-semibold')"
        " and contains(@class,'text-[#334155]')])[1]",
    )
    take_down_button = ("xpath", "(//button[normalize-space()='下架'])[last()]")
    confirm_take_down_button = ("xpath", "(//button[normalize-space()='确认下架'])[last()]")
    official_skill_title = (
        "xpath",
        "//div[contains(@class,'text-[16px]')"
        " and contains(@class,'font-extrabold')"
        " and contains(@class,'truncate')"
        " and not(ancestor::*[contains(@class,'arco-message')"
        " or contains(@class,'arco-notification')"
        " or contains(@class,'arco-modal')"
        " or contains(@class,'arco-drawer')])]",
    )
    ignored_title_lines = {
        "技能",
        "我的技能",
        "我创建的",
        "技能商店",
        "官方技能",
        "官方",
        "全部技能",
        "全部",
        "团队",
        "团队技能",
        "上架到技能商店",
        "上架技能商店",
        "上架到团队",
        "即刻运行",
        "添加到我的技能",
        "确认添加",
        "确认上架",
        "下架",
        "确认下架",
        "确认",
        "确定",
        "编辑",
        "删除",
    }

    # 进入技能页。
    def open_skills_page(self) -> None:
        self.driver.get(f"{settings.base_url.rstrip('/')}{self.skills_path}")
        self.wait_visible(self.skill_menu, timeout=20)

    # 打开创建技能面板。
    def open_create_skill_panel(self) -> None:
        self.click(self.skill_menu, timeout=15)
        self.click(self.create_skill_button, timeout=15)

    # 输入第一条技能创作指令并点击发送。
    def submit_first_instruction(self, prompt: str) -> None:
        prompt_input = self.wait_visible(self.first_instruction_input, timeout=15)
        prompt_input.clear()
        prompt_input.send_keys(prompt)
        self.click(self.send_button, timeout=10)

    # 等待生成结果出现，并把生成的技能添加到我的技能。
    def add_generated_skill(self) -> bool:
        self.click(self.add_to_my_skills_button, timeout=120)
        self.click(self.confirm_add_button, timeout=20)
        return self.wait_invisible(self.confirm_add_button, timeout=20)

    # 按完整流程创建技能：打开面板、发送指令、确认添加。
    def create_skill_from_prompt(self, prompt: str) -> bool:
        self.open_create_skill_panel()
        self.submit_first_instruction(prompt)
        return self.add_generated_skill()

    # 进入技能模块下的“我的技能 -> 我创建的”列表。
    def open_my_created_skills(self) -> None:
        self.click(self.skill_menu, timeout=20)
        self.click(self.my_skills_tab, timeout=20)
        self.click(self.my_created_tab, timeout=20)

    # 进入技能模块下的“技能商店”页签。
    def open_skill_store(self) -> None:
        self.click(self.skill_menu, timeout=20)
        self.click(self.skill_store_tab, timeout=20)

    # 打开技能商店里的官方技能列表。
    def open_official_skills(self) -> None:
        self.open_skill_store()
        self.click(self.official_tab, timeout=20)

    # 打开技能商店里的全部技能列表。
    def open_all_skills(self) -> None:
        self.open_skill_store()
        self.click(self.all_tab, timeout=20)

    # 打开技能商店里的团队技能列表。
    def open_team_skills(self) -> None:
        self.open_skill_store()
        self.click(self.team_tab, timeout=20)

    # 构造可安全放入 XPath 表达式的文本字面量。
    def _xpath_literal(self, value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    # 从元素文本里提取技能名称，过滤掉按钮和页签文案。
    def _title_from_text(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines:
            if line not in self.ignored_title_lines:
                return line
        return ""

    # 从操作按钮向上查找所属技能卡片，并提取该技能名称。
    def _skill_name_near_button(self, button: WebElement) -> str:
        for level in range(1, 10):
            card = button.find_element(By.XPATH, f"./ancestor::*[{level}]")
            title = self._title_from_text(card.text)
            if title:
                return title
        return ""

    # 获取第一个指定操作按钮及其所属技能名称，遇到前端重渲染会重试。
    def _button_and_skill_name(self, locator: tuple[str, str]) -> tuple[WebElement, str]:
        last_error = None
        for _ in range(3):
            try:
                button = self.wait_clickable(locator, timeout=20)
                skill_name = self._skill_name_near_button(button)
                if not skill_name:
                    raise AssertionError("未获取到技能名称，无法验证后续列表")
                return button, skill_name
            except StaleElementReferenceException as error:
                last_error = error
        raise last_error

    # 点击确认谈弹窗按钮。
    def _click_first_available(self, locator: tuple[str, str]) -> bool:
        if self.is_visible(locator, timeout=4):
            self.click(locator, timeout=4)
            return True
        return False  

    # 等待上架团队弹窗出现，并选择列表中的第一个团队。
    def select_first_team_in_publish_modal(self, timeout: int = 20) -> None:
        self.wait_visible(self.team_publish_modal, timeout=timeout)
        self.click(self.first_team_in_publish_modal, timeout=timeout)

    # 获取第一个可见且有文本的元素，避免其他页签隐藏内容干扰。
    def _first_visible_text_element(self, locator: tuple[str, str], timeout: int = 20) -> WebElement:
        def find_visible_text_element(driver: WebDriver) -> WebElement | bool:
            for element in driver.find_elements(*locator):
                text = element.text.strip()
                if element.is_displayed() and text and text not in self.ignored_title_lines:
                    return element
            return False

        return WebDriverWait(self.driver, timeout).until(
            find_visible_text_element,
            message=f"未找到可见文本元素: {locator}",
        )

    # 点击当前列表中的指定技能，进入技能详情弹窗。
    def open_skill_detail(self, skill_name: str) -> None:
        skill_locator = (
            "xpath",
            f"//*[normalize-space()={self._xpath_literal(skill_name)}"
            " and not(ancestor::*[contains(@class,'arco-message')"
            " or contains(@class,'arco-notification')"
            " or contains(@class,'arco-modal')"
            " or contains(@class,'arco-drawer')])]",
        )
        skill = self.wait_clickable(skill_locator, timeout=20)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", skill)
        skill.click()

    # 点击官方技能列表中的第一个技能，返回该技能名称。
    def open_first_official_skill_detail(self) -> str:
        title = self._first_visible_text_element(self.official_skill_title, timeout=20)
        skill_name = title.text.strip()
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title)
        title.click()
        return skill_name

    # 从官方技能列表打开指定技能，并在详情弹窗中下架。
    def take_down_official_skill(self, skill_name: str) -> str:
        self.open_official_skills()
        self.open_skill_detail(skill_name)
        self.click(self.take_down_button, timeout=20)
        self.click(self.confirm_take_down_button, timeout=20)
        self.wait_invisible(self.confirm_take_down_button, timeout=20)
        return skill_name

    # 从官方技能列表打开第一个技能，并在详情弹窗中下架。
    def take_down_first_official_skill(self) -> str:
        self.open_official_skills()
        skill_name = self.open_first_official_skill_detail()
        self.click(self.take_down_button, timeout=20)
        self.click(self.confirm_take_down_button, timeout=20)
        self.wait_invisible(self.confirm_take_down_button, timeout=20)
        return skill_name

    # 在“我创建的”列表中按技能名称定位对应卡片，再验证该卡片里的按钮状态。
    def is_created_skill_store_status_visible(
        self,
        skill_name: str,
        status_text: str = "已上架技能商店",
        timeout: int = 20,
    ) -> bool:
        self.open_my_created_skills()
        skill_literal = self._xpath_literal(skill_name)
        status_literal = self._xpath_literal(status_text)
        locator = (
            "xpath",
            f"//*[normalize-space()={skill_literal}"
            " and not(ancestor::*[contains(@class,'arco-message')"
            " or contains(@class,'arco-notification')"
            " or contains(@class,'arco-modal')"
            " or contains(@class,'arco-drawer')])]"
            "/ancestor::*[contains(concat(' ', normalize-space(@class), ' '), ' group ')][1]"
            f"//button[contains(normalize-space(.), {status_literal})]",
        )
        return self.is_visible(locator, timeout=timeout)

    # 在“我创建的”列表中选择第一个技能并上架到技能商店，返回技能名称。
    def publish_first_created_skill_to_store(self) -> str:
        self.open_my_created_skills()
        button, skill_name = self._button_and_skill_name(self.publish_to_store_button)
        button.click()
        self.click(self.confirm_publish_button, timeout=20)
        self.wait_invisible(self.confirm_publish_button, timeout=20)
        return skill_name

    # 在“我创建的”列表中选择第一个技能并上架到团队，返回技能名称。
    def publish_first_created_skill_to_team(self) -> str:
        self.open_my_created_skills()
        button, skill_name = self._button_and_skill_name(self.publish_to_team_button)
        button.click()
        self.select_first_team_in_publish_modal(timeout=20)
        self.click(self.confirm_publish_button, timeout=20)
        self.wait_invisible(self.team_publish_modal, timeout=20)
        return skill_name

    # 在“我创建的”列表中选择第一个技能并点击即刻运行，返回技能名称。
    def run_first_created_skill(self) -> str:
        self.open_my_created_skills()
        button, skill_name = self._button_and_skill_name(self.run_now_button)
        button.click()
        return skill_name

    # 判断对话页输入框容器中是否默认选择了指定技能。
    def is_skill_selected_near_chat_input(self, skill_name: str, timeout: int = 20) -> bool:
        def skill_name_in_chat_input_container(driver: WebDriver) -> bool:
            for container in driver.find_elements(*self.chat_input_container):
                if not container.is_displayed():
                    continue

                container_text = container.text or container.get_attribute("textContent") or ""
                if skill_name in container_text:
                    return True

            return False

        try:
            WebDriverWait(self.driver, timeout).until(
                skill_name_in_chat_input_container,
                message=f"对话页输入框容器未默认选择技能: {skill_name}",
            )
            return True
        except TimeoutException:
            return False

    # 判断点击即刻运行后是否已自动跳转到对话页面。
    def is_conversation_page_visible(self, timeout: int = 20) -> bool:
        def conversation_tab_selected(driver: WebDriver) -> bool:
            try:
                for element in driver.find_elements(*self.conversation_tab):
                    if not element.is_displayed():
                        continue

                    if element.is_selected() or element.get_attribute("aria-selected") == "true":
                        return True

                    for level in range(1, 5):
                        ancestor = element.find_element(By.XPATH, f"./ancestor::*[{level}]")
                        class_name = ancestor.get_attribute("class") or ""
                        aria_selected = ancestor.get_attribute("aria-selected")
                        if aria_selected == "true" or any(
                            selected_class in class_name
                            for selected_class in ("active", "selected", "checked")
                        ):
                            return True

                return False
            except StaleElementReferenceException:
                return False

        try:
            WebDriverWait(self.driver, timeout).until(
                conversation_tab_selected,
                message="点击即刻运行后对话页签未选中",
            )
            return True
        except TimeoutException:
            return False

    # 判断对话页是否自动选中易法通AI。
    def is_yifatong_ai_selected(self, timeout: int = 10) -> bool:
        return self.is_visible(self.ai_selector, timeout=timeout)

    # 判断当前页面是否可见指定文本。
    def is_text_visible(self, text: str, timeout: int = 10) -> bool:
        locator = ("xpath", f"//*[text()[contains(normalize-space(.), {self._xpath_literal(text)})]]")
        return self.is_visible(locator, timeout=timeout)

    # 构造技能商店列表中指定技能的定位，避开提示消息和弹窗。
    def _store_skill_locator(self, skill_name: str) -> tuple[str, str]:
        return (
            "xpath",
            f"//*[text()[contains(normalize-space(.), {self._xpath_literal(skill_name)})]"
            " and not(ancestor::*[contains(@class,'arco-message')"
            " or contains(@class,'arco-notification')"
            " or contains(@class,'arco-modal')"
            " or contains(@class,'arco-drawer')])]",
        )

    # 判断技能商店当前列表中是否可见指定技能。
    def is_store_skill_visible(self, skill_name: str, timeout: int = 20) -> bool:
        locator = self._store_skill_locator(skill_name)
        return self.is_visible(locator, timeout=timeout)

    # 等待技能商店当前列表中已不存在指定技能。
    def is_store_skill_absent(self, skill_name: str, timeout: int = 20) -> bool:
        locator = self._store_skill_locator(skill_name)

        def no_visible_skill(driver: WebDriver) -> bool:
            try:
                return not any(element.is_displayed() for element in driver.find_elements(*locator))
            except StaleElementReferenceException:
                return False

        try:
            WebDriverWait(self.driver, timeout).until(
                no_visible_skill,
                message=f"等待技能从当前列表消失超时: {skill_name}",
            )
            return True
        except TimeoutException:
            return False

    # 在技能商店官方列表中验证技能是否可见。
    def is_skill_visible_in_official_store(self, skill_name: str, timeout: int = 20) -> bool:
        self.open_official_skills()
        return self.is_store_skill_visible(skill_name, timeout=timeout)

    # 在技能商店官方列表中验证技能是否已不存在。
    def is_skill_absent_in_official_store(self, skill_name: str, timeout: int = 20) -> bool:
        self.open_official_skills()
        return self.is_store_skill_absent(skill_name, timeout=timeout)

    # 在技能商店全部列表中验证技能是否可见。
    def is_skill_visible_in_all_store(self, skill_name: str, timeout: int = 20) -> bool:
        self.open_all_skills()
        return self.is_store_skill_visible(skill_name, timeout=timeout)

    # 在技能商店全部列表中验证技能是否已不存在。
    def is_skill_absent_in_all_store(self, skill_name: str, timeout: int = 20) -> bool:
        self.open_all_skills()
        return self.is_store_skill_absent(skill_name, timeout=timeout)

    # 等待跳转到对话页，并确认易法通AI已出现。
    def wait_for_conversation_ready(self) -> None:
        self.wait_visible(self.conversation_tab, timeout=20)
        self.wait_visible(self.ai_selector, timeout=20)
