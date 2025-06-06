from django.shortcuts import render
from myadmin.models import Product
from pyecharts.charts import basic_charts
from django.http import HttpResponse, JsonResponse
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Line
import pandas as pd
import json
import random
from rest_framework.views import APIView
from pyecharts.faker import Faker


# CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("././templates/mychart"))

# 用echart显示动态数据（采用javascript)
def index(request):
    demos = Product.objects.all()
    demos = demos.order_by("price")
    list1 = []
    list2 = []
    for demo in demos:
        list1.append(demo.name)
        list2.append(demo.price)
    # df = pd.DataFrame({'values': list2, 'name': list1})

    context = {"product_list": list1, 'price_list': list2}
    #return render(request, 'mytest/test1.html', context)
    return render(request, 'index.html', context)
    # 下面这条是返回静态数据页面
    # return render(request, "mytest/info.html")
def index0(request):

    return render(request, 'index.html')
    # 下面这条是返回静态数据页面
    # return render(request, "mytest/info.html")

# 南丁格尔图示例
def index3(request):
    return render(request, 'mytest/rosepic.html')


def index2(request):
    # 准备数据
    provinces = ['北京', '上海', '黑龙江', '吉林', '辽宁', '内蒙古', '新疆', '西藏', '青海', '四川', '云南', '陕西', '重庆',
                 '贵州', '广西', '海南', '澳门', '湖南', '江西', '福建', '安徽', '浙江', '江苏', '宁夏', '山西', '河北', '天津']
    num = [1, 1, 1, 17, 9, 22, 23, 42, 35, 7, 20, 21, 16, 24, 16, 21, 37, 12, 13, 14, 13, 7, 22, 8, 16, 13, 13]
    color_series = ['#FAE927', '#E9E416', '#C9DA36', '#9ECB3C', '#6DBC49',
                    '#37B44E', '#3DBA78', '#14ADCF', '#209AC9', '#1E91CA',
                    '#2C6BA0', '#2B55A1', '#2D3D8E', '#44388E', '#6A368B',
                    '#7D3990', '#A63F98', '#C31C88', '#D52178', '#D5225B',
                    '#D02C2A', '#D44C2D', '#F57A34', '#FA8F2F', '#D99D21',
                    '#FA1F7F', '#D5534']
    # print(type(color_series))

    # 创建数据框
    df = pd.DataFrame({'provinces': provinces, 'num': num})

    # 导入数据
    # df = pd.read_excel('data.xlsx')

    df.sort_values(by='num', ascending=False, inplace=True)

    v = df['provinces'].values.tolist()
    d = df['num'].values.tolist()

    df['color_series'] = color_series

    color_series = df['color_series'].values.tolist()

    pie1 = Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
    # 设置颜色
    pie1.set_colors(color_series)
    # 添加数据，设置饼图的半径，是否展示成南丁格尔图
    pie1.add("", [list(z) for z in zip(v, d)],
             radius=["30%", "135%"],
             center=["50%", "65%"],
             rosetype="area"
             )
    # 设置全局配置项
    pie1.set_global_opts(title_opts=opts.TitleOpts(title='玫瑰图示例'),
                         legend_opts=opts.LegendOpts(is_show=False),
                         toolbox_opts=opts.ToolboxOpts())
    # 设置系列配置项
    pie1.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12,
                                                   formatter="{b}:{c}天", font_style="italic",
                                                   font_weight="bold", font_family="Microsoft YaHei"
                                                   ),
                         )
    # 生成html文档
    pie1.render('templates/mytest/rosepic.html')
    return render(request, "mytest/nandinggeer.html")


# 用Pyecharts显示数据的方法（静态数据）
# Pyecharts是一款使用Python对Echarts进行再次封装后的开源框架
def draw_fig(request):
    c = (Bar().add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]).add_yaxis("商家A", [5, 20, 36, 10, 75, 90]).add_yaxis(
        "商家B", [15, 25, 16, 55, 48, 8]).set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题")))
    return HttpResponse(c.render_embed())


def draw_fig2(request):
    demos = Product.objects.all()
    list1 = []
    list2 = []
    for demo in demos:
        list1.append(demo.name)
        list2.append(demo.price)

    c = (Bar().add_xaxis(list1).add_yaxis("商家A", list2))
    # 生成render.html文件
    c.savefig
    c.render()
    return HttpResponse(c.render_embed())


def draw_fig3(request):
    random_list = []
    chart = []
    for j in range(20):
        random_list.append(random.randint(1, 20))
    return json.dumps(random_list)


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data: object, code: object = 200) -> object:
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


def pie_base() -> Pie:
    c = (
        Pie()
            .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
            .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-示例"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .dump_options_with_quotes()
    )
    return c


def bar_base() -> Bar:
    c = (
        Bar()
            .add_xaxis(["衬衫1", "衬衫2", "衬衫3", "衬衫4", "衬衫5", "衬衫6"])
            .add_yaxis("商家A", [random.randrange(0, 100) for _ in range(6)])
            .add_yaxis("商家B", [random.randrange(0, 100) for _ in range(6)])
            .set_global_opts(title_opts=opts.TitleOpts(title="bar示例"))
            .dump_options_with_quotes()
    )
    return c


class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(bar_base()))


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/mytest/test2.html").read())


def line_base() -> Line:
    line = (
        Line()
            .add_xaxis(["{}".format(i) for i in range(10)])
            .add_yaxis(
            series_name="",
            y_axis=[random.randrange(50, 80) for _ in range(10)],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="动态数据"),
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
            .dump_options_with_quotes()
    )
    return line


class ChartView2(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(line_base()))


global cnt
cnt = 9


class ChartUpdateView2(APIView):
    def get(self, request, *args, **kwargs):
        global cnt
        cnt = cnt + 1
        return JsonResponse({"name": cnt, "value": random.randrange(0, 100)})
