import os
import pytest

if __name__ == "__main__":
    # 第一步：运行 pytest，指定 allure 结果目录（my_allure_results）
    # 添加 --clean-alluredir 确保每次运行清理旧结果
    pytest.main(["-vs","--alluredir=my_allure_results", "--clean-alluredir"])

    # 第二步：生成 allure 报告（确保结果目录已生成）
    # 检查目录是否存在，避免报错
    if os.path.exists("my_allure_results"):
        os.system("allure generate -o report -c my_allure_results")
    else:
        print("错误：my_allure _results 目录未生成，请检查 pytest 配置")