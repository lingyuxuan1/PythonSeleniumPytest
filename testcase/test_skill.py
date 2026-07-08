from datetime import datetime

import allure
import pytest

from common.datas import get_data
from page.skill_page import SkillPage


class TestSkill:
    test_data = get_data()
    skill_data = test_data.read_excel_skill_data()

    # 验证用户登录后可以根据 Excel 中的指令创建技能，并添加到我的技能。
    # @allure.feature("技能")
    # @allure.story("创建技能")
    # @pytest.mark.parametrize("case", skill_data)
    # def test_create_skill_flow(self, login_driver, case):
    #     allure.dynamic.title(case.get("case_name", "创建技能流程"))

    #     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    #     prompt_template = case["prompt"]
    #     prompt = prompt_template.replace("{timestamp}", timestamp)

    #     skill_page = SkillPage(login_driver)
    #     assert skill_page.create_skill_from_prompt(prompt), "确认添加后弹窗未关闭，创建技能流程失败"

    # # 验证我创建的技能上架到技能商店后，可以在官方技能和全部技能列表中看到。
    # @allure.feature("技能")
    # @allure.story("上架到技能商店")
    # def test_publish_skill_to_store(self, login_driver):
    #     skill_page = SkillPage(login_driver)
    #     skill_page.open_skills_page()
    #     skill_name = skill_page.publish_first_created_skill_to_store()

    #     assert skill_page.is_skill_visible_in_official_store(skill_name), "官方技能列表未找到已上架技能"
    #     assert skill_page.is_skill_visible_in_all_store(skill_name), "全部技能列表未找到已上架技能"

    # # 验证官方技能下架后，我创建的技能列表中出现上架技能商店状态。
    # @allure.feature("技能")
    # @allure.story("下架官方技能")
    # def test_take_down_official_skill_and_check_created_status(self, login_driver):
    #     skill_page = SkillPage(login_driver)
    #     skill_page.open_skills_page()
    #     skill_name = skill_page.take_down_first_official_skill()

    #     assert skill_page.is_created_skill_store_status_visible(
    #         skill_name,
    #         status_text="上架技能商店",
    #     ), "我创建的技能列表中对应技能未显示已上架技能商店按钮"
    #     assert skill_page.is_skill_absent_in_all_store(skill_name), "全部技能列表仍显示已下架技能"
    #     assert skill_page.is_skill_absent_in_official_store(skill_name), "官方技能列表仍显示已下架技能"

    # # 验证我创建的技能选择第一个团队上架后，可以在技能商店的团队列表中看到。
    # @allure.feature("技能")
    # @allure.story("上架到团队")
    # def test_publish_skill_to_team(self, login_driver):
    #     skill_page = SkillPage(login_driver)
    #     skill_page.open_skills_page()
    #     skill_name = skill_page.publish_first_created_skill_to_team()

    #     skill_page.open_team_skills()
    #     assert skill_page.is_text_visible(skill_name, timeout=10), "团队列表未找到已上架技能"

    # # 验证点击即刻运行后跳转到对话页，并自动选中易法通AI和该技能。
    # @allure.feature("技能")
    # @allure.story("即刻运行")
    # def test_run_skill_jump_to_dialog(self, login_driver):
    #     skill_page = SkillPage(login_driver)
    #     skill_page.open_skills_page()
    #     skill_name = skill_page.run_first_created_skill()

    #     assert skill_page.is_conversation_page_visible(
    #         timeout=20,
    #     ), "点击即刻运行后未自动跳转到对话页面"
    #     assert skill_page.is_yifatong_ai_selected(timeout=10), "对话页未自动选中易法通AI"
    #     assert skill_page.is_skill_selected_near_chat_input(
    #         skill_name,
    #         timeout=20,
    #     ), "对话页输入框容器未默认选择该技能"
