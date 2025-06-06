
# 员工信息管理视图文件
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from myadmin.models import Order2
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.db.models import Avg, Max, Min, Count, Sum


def index(request, p_index=1):
    """浏览信息"""
    umod = Order2.objects.all()

    ulist = umod.filter(status__lt=9)

    ulist = ulist.order_by("id")  # 对id排序
    #查询
    kw = request.GET.get("keyword", None)
    if kw:
        ulist = ulist.filter(Q(shopname__contains=kw) | Q(id__contains=kw)) #根据Orders2视图中选取shopname或者店铺id查询
    #按照状态status字段进行查询
    status = None
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
    # 显示所有数据代码：
    context = {"user_list": ulist,"selectstatus": status}
    return render(request, "myadmin/orders/index.html", context)