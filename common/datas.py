import csv
import openpyxl

class get_data:
    def read_execel_login(self):
        workbook = openpyxl.load_workbook('D:/YFT/PythonSeleniumPytest/data/登录数据.xlsx')
        worksheet = workbook['Sheet1']
        data = []
        for row in worksheet.iter_rows(min_row=2,values_only=True):
            data.append(row)
        workbook.close()
        return (data)

    def read_excel_login_data(self):
        workbook1 = openpyxl.load_workbook('D:/YFT/PythonSeleniumPytest/data/登录接口请求测试数据.xlsx')
        worksheet1 = workbook1['Sheet1']
        data = []
        keys = [cell.value for cell in worksheet1[2]]
        for row in worksheet1.iter_rows(min_row=3,max_row=4,values_only=True):
            dict_data = dict(zip(keys, row))
            data.append(dict_data)
        workbook1.close()
        return (data)

getdata = get_data()
print(getdata.read_execel_login())


