# import  json
from pyecharts.charts import Line, Map,Bar
from pyecharts.options import TitleOpts, LegendOpts, ToolboxOpts, VisualMapOpts

# data = [{"name":"张一","age":18},{"name":"张二","age":18},{"name":"张三","age":18}]
# json_str = json.dumps(data,ensure_ascii=False)
# print(json_str)
#
# data1 = {"name":"张一","age":18}
# json_str1 = json.dumps(data1,ensure_ascii=False)
# print(json_str1)
#
# data2 = '[{"name":"张一","age":18},{"name":"张二","age":18},{"name":"张三","age":18}]'
# json_str2 = json.loads(data2)
# print(json_str2)

#折线图
# line1 = Line()
# line1.add_xaxis(["中国","美国","英国"])
# line1.add_yaxis("GDP",[30,20,10])
# line1.set_global_opts(
#     title_opts=TitleOpts(title = "GDP展示",pos_left="center",pos_bottom="1%"),
#     legend_opts=LegendOpts(is_show=True),
#     toolbox_opts=ToolboxOpts(is_show=True),
#     visualmap_opts=VisualMapOpts(is_show=True)
# )
# line1.render()

#地图可视化 Map模块
# map = Map()
# data = [
#     ("北京",99)
# ]
# map.add("测试地图",data,"china")
# map.render()

#柱状图
# bar = Bar()
# bar.add_xaxis(["中国","美国","英国"])
# bar.add_yaxis("GDP",[30,20,10])
# bar.reversal_axis()
# dict_1 = {"a":1}
# print(dict_1.values())
#
# a = range(1,10)
# print(a)
# name = input('111111')  # 括号里是提示文字（可选）
# print("你输入的姓名是：", name)
a =1
b =2

if a == b:
    print(a)
else:
    print(b)






