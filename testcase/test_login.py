from time import sleep
import requests
from page.login_page import *
from common.datas import *
import pytest
from common.setting import settings
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, expected_conditions


class TestLogin:
    plaintext_button = ('xpath', "//span[@class='arco-icon-hover']")
    active_button = ('xpath', "//input[@autocomplete='current-password']")
    getdata = get_data()
    getdata1_1 = getdata.read_execel_login()
    data1 = [row for row in getdata1_1[:1]]
    @pytest.mark.parametrize("username,password", data1)
    # 正向流程
    def test_login(self, username,password,driver):
        driver.get(settings.base_url)  # 重置到登录页
        self.lp = LoginPage(driver)
        a= self.lp.do_login(username,password)
        assert a in "我的","登录正向功能报错"

    # 手机号为空、10位数、12位数、数字以外的其他字符
    data2 = [row for row in getdata1_1[1:5]]
    @pytest.mark.parametrize("username,password", data2)
    def test1(self,username,password,driver):
        driver.get(settings.base_url)
        self.lp = LoginPage(driver)
        error = self.lp.login_phone(username, password)
        assert error in  "请输入手机号","手机号必填提示验证语不符"
    #
    # 密码必填
    data3 = [row[0] for row in getdata1_1[5:6]]
    @pytest.mark.parametrize("username",data3)
    def test2(self, username, driver):
        driver.get(settings.base_url)
        self.lp = LoginPage(driver)
        error = self.lp.login_pwd(username, '')
        assert error in  "密码不可为空", "密码必填必填提示验证语不符"
    #
    # 未注册手机号登录、密码错误
    data4 = get_data().read_excel_login_data()
    @pytest.mark.parametrize("case",data4)
    def test3(self,case):
        #解决字符串变成字典问题eval()函数,可以将str当成有效字符串并计算里面值，比如是s= ”len('hello')“ print(eval(s))=5
        method = case['method']
        url = 'https://rag.yifatong.com/'+case['path']
        headers = eval(case['headers']) if isinstance(case['headers'], str) else None
        params = case['params'] if isinstance(case['params'], str) else None
        data = case['data'] if isinstance(case['data'], str) else None
        json = eval(case['json']) if isinstance(case['json'], str) else None
        files = case['files']

        request_data = {
            'method': method,
            'url': url,
            'headers': headers,
            'params': params,
            'data': data,
            'json': json,
            'files': files
        }
        # print(request_data)
        resp = requests.request(**request_data)
        print(resp.json())
        assert resp.json()['message'] == '手机号不存在或密码错误','手机号未注册登录提示语错误或密码错误提示语错误'



    #密码明文显示验证
    def test4(self, driver):
        driver.get(settings.base_url)
        self.lp = LoginPage(driver)
        self.lp.login_page()

        # 1. 先定位 密码框 和 明文/暗文切换按钮
        pwd_input = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located(self.active_button)
        )
        toggle_btn = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located(self.plaintext_button)
        )

        # ==============================================
        # 第一步：初始状态 → 暗文（password）
        # ==============================================
        assert pwd_input.get_attribute("type") == "password", "初始不是暗文"
        print("✅ 初始状态：暗文")

        # ==============================================
        # 第二步：点击一次 → 切换成明文（text）
        # ==============================================
        toggle_btn.click()
        sleep(1)
        assert pwd_input.get_attribute("type") == "text", "切换明文失败"
        print("✅ 点击一次：明文")

        # ==============================================
        # 第三步：再点击一次 → 切回暗文（password）
        # ==============================================
        toggle_btn.click()
        sleep(1)
        assert pwd_input.get_attribute("type") == "password", "切回暗文失败"
        print("✅ 再次点击：切回暗文")

        print("🎉 暗文→明文→暗文 全流程通过！")

    #验证码登录

    data5 = [row[0] for row in getdata1_1[7:8]]
    @pytest.mark.verification
    @pytest.mark.parametrize('phone_number', data5)
    def test5(self, phone_number,driver):
        self.lp = LoginPage(driver)
        message = self.lp.verify_login(phone_number)
        wait = WebDriverWait(driver, 10).until(
            lambda b:not message.is_enabled(),
            message="按钮未变为不可用（倒计时未开始）"
        )
        assert message.is_enabled() is False,'验证码发送失败：按钮文案未切换倒计时'