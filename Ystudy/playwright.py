from  playwright.sync_api import  sync_playwright

p = sync_playwright()
page = p.new_page()
page.goto("https://www.baidu.com/")