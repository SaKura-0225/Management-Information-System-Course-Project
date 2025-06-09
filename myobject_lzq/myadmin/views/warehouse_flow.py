#出入库管理视图文件
from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.shortcuts import redirect
from django.urls import reverse
import re
from myadmin.models import Orders,User,Shop
from django.db.models import Avg,Max,Min,Count,Sum


def index(request):
    return render(request, 'myadmin/warehouse-flow/index.html')  

def add_to_inventory(item, quantity):
    # 入库逻辑
    pass

def remove_from_inventory(item, quantity):
    # 出库逻辑
    pass

def check_inventory(item):
    # 检查库存
    pass