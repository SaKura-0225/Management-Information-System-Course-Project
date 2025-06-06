# 测试图表路由
from django.urls import path

from myadmin.views import index
from myadmin.views import user
from myadmin.views import shop
from myadmin.views import category, product, member
from mytest import views

urlpatterns = [
    path('', views.index, name="mytest_index"),
    path('show_pic/', views.index3, name="show_pic"),
    path('chart/', views.draw_fig, name="mytest_draw"),
    path('chart2/', views.draw_fig3, name="mytest_draw2"),
    path('pie/', views.ChartView.as_view(), name='demo'),
    path('index/', views.IndexView.as_view(), name='demo'),
    path('bar/', views.ChartView.as_view(), name='demo'),
    path('barUpdate/', views.ChartView.as_view(), name='demo'),
    path('line/', views.ChartView2.as_view(), name='demo'),
    path('lineUpdate/', views.ChartUpdateView2.as_view(), name='demo')

]

