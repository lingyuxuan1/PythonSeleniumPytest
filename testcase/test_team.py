from datetime import datetime

import allure

from page.team_page import TeamPage


class TestTeam:
    # 验证进入团队页后，可以创建我的团队，并在创建完成后看到该团队。
    # @allure.feature("团队")
    # @allure.story("创建我的团队")
    # def test_create_my_team(self, login_driver):
    #     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    #     team_name = f"自动化测试团队{timestamp}"
    #     description = f"自动化创建团队描述{timestamp}"

    #     team_page = TeamPage(login_driver)
    #     team_page.open_team_page()

    #     assert team_page.create_team(team_name, description), "点击完成创建后未创建成功"
    #     assert team_page.is_team_visible(team_name, timeout=20), "团队列表中未找到新创建的团队"

    # 验证进入团队页后，可以创建官方团队，并在创建完成后看到该团队。
    @allure.feature("团队")
    @allure.story("创建官方团队")
    def test_create_official_team(self, login_driver):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        team_name = f"自动化官方团队{timestamp}"
        description = f"自动化创建官方团队描述{timestamp}"

        team_page = TeamPage(login_driver)
        team_page.open_team_page()

        assert team_page.create_official_team(team_name, description), "点击完成创建后未创建官方团队成功"
        assert team_page.is_team_visible(team_name, timeout=20), "团队列表中未找到新创建的官方团队"
