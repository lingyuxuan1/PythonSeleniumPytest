from common.com import Baseclass
from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement


class LoginPage(Baseclass):
#     # 页面元素定位器
    #登录页面
    login_button =("xpath","//*[@id='app']/div/div/section/main/div/div[2]/div[1]/button")
    #手机号
    hc_phone = ("xpath","//input[@placeholder='请输入手机号']")
    #密码
    hc_password = ("xpath","//input[@placeholder='请输入密码']")
    #登录按钮
    hc_loginBtn = ("xpath","(//button)[3]")
    #判断登录成功
    login_success = ('xpath',"//span[contains(text(),'我的')]")
    #验证号码错误提示信息
    phone_error = ('xpath', "//div[@class = 'arco-form-item-message' and text() = '请输入手机号']")
    pwd_error =('xpath', "//div[text() = '密码不可为空']")

    #验证码登录按钮
    Verification_button = ('xpath',"//span[text()='验证码登录']")
    #获取验证码按钮
    get_verification_button = ('xpath',"//button[text()='获取验证码']")

    #技能
    skill = ('xpath',"//span[text() = '技能']")
    #创建技能
    create_skill = ('xpath',"/button[text()=' 创建技能 ']")
    #技能输入框
    skill_inpute = ('css',"input[placeholder='在此输入您的第一个指令，开启 AI 技能创作...']")
    #发送按钮
    send_button = ('css',"svg.lucide-arrow-up")
    #添加到我的技能
    add_skill = ('xpath',"//button[text()='添加到我的技能']")

    def login_page(self) -> None:
        """打开登录弹窗。"""
        # #登录弹窗
        login = self.wait_clickable(self.login_button, 10)
        login.click()

    def do_login(self, username: str, password: str) -> str:
        """输入账号密码并登录，返回登录结果文本。"""
        #获取网址
        # self.get_url(self.hc_url)
        # #登录弹窗
        login = self.wait_clickable(self.login_button,10)
        login.click()
        #输入手机号
        phone = self.wait_visible(self.hc_phone,5)
        # phone.click()
        phone.send_keys(username)
        #输入密码
        pas = self.wait_visible(self.hc_password,5)
        # pas.click()
        pas.send_keys(password)
        # #等待弹窗框消失
        # cancel = self.wait_invisible(self.invisible,5)
        #点击登录按钮
        click_login_button = self.wait_clickable(self.hc_loginBtn,5)
        click_login_button.click()
        try:
            asure = self.wait_visible(self.login_success, 5)
        except TimeoutException:  # 这里必须是这个！
            return "登录失败"
        else:
            if asure:
                return asure.text

    def login_phone(self, username: str, password: str) -> str:
        """提交登录表单后返回手机号错误提示。"""
        login = self.wait_clickable(self.login_button,10)
        login.click()
        # 输入手机号
        phone = self.wait_visible(self.hc_phone, 5)
        phone.send_keys(username)
        # 输入密码
        pas = self.wait_visible(self.hc_password, 5)
        pas.send_keys(password)
        # 点击登录按钮
        click_login_button = self.wait_clickable(self.hc_loginBtn, 5)
        click_login_button.click()
        #定位手机号错误提示
        return self.wait_visible(self.phone_error, 5).text

    def login_pwd(self, username: str, password: str) -> str:
        """提交登录表单后返回密码错误提示。"""
        login = self.wait_clickable(self.login_button, 10)
        login.click()
        # 输入手机号
        phone = self.wait_visible(self.hc_phone, 5)
        phone.send_keys(username)
        # 输入密码
        pas = self.wait_visible(self.hc_password, 5)
        pas.send_keys(password)
        # 点击登录按钮
        click_login_button = self.wait_clickable(self.hc_loginBtn, 5)
        click_login_button.click()
        # 定位密码错误提示
        return self.wait_visible(self.pwd_error, 5).text

    def verify_login(self, phone_number: str) -> WebElement:
        """切换到验证码登录并获取验证码按钮元素。"""
        self.login_page()
        located_Verification_button = self.wait_clickable(self.Verification_button, 5)
        located_Verification_button.click()
        phone = self.wait_visible(self.hc_phone, 5)
        phone.send_keys(phone_number)
        #获取验证码
        located_get_verification_button = self.wait_clickable(self.get_verification_button, 5)
        located_get_verification_button.click()

        located_Verification_button1 = self.wait_clickable(self.get_verification_button, 5)
        return located_Verification_button1

    #创建技能正向流程
    # def create_skill(self,keyword):



