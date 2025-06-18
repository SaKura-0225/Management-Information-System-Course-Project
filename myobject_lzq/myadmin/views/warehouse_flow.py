
# 出入库信息管理视图文件
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from collections import defaultdict
from datetime import datetime, timedelta
# Create your views here.
from myadmin.models import WmsOutbound
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.db.models import Avg, Max, Min, Count, Sum
from .forms import AddWarehouseInfoForm
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay



def inbound_index(request):
    return render(request, 'myadmin/warehouse-flow/inbound_index.html')  

def outbound_index(request):
    outbound = WmsOutbound.objects.all()
    outbound_list = outbound.order_by("id")  # 对id排序
    #查询
    kw = request.GET.get("keyword", None)
    if kw:
        outbound_list = outbound_list.filter(Q(orders_id__contains=kw)) #根据视图中选取订单编号查询
    paginator = Paginator(outbound_list, 4)  # Show 1 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # 显示所有数据代码：
    context = {"outbound_list": outbound_list,"page_obj": page_obj}
    return render(request, 'myadmin/warehouse-flow/outbound_index.html', context)


def add_outbound(request):
    if request.method == "POST":
        form = AddWarehouseInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myadmin_warehouse-flow_outbound')
    else:
        form =AddWarehouseInfoForm()
    return render(request, 'myadmin/warehouse-flow/add.html', {'form':form})


def edit_outbound(request, id):
    outbound = WmsOutbound.objects.get(pk=id)
    if request.method == "POST":
        form = AddWarehouseInfoForm(request.POST, instance=outbound)
        if form.is_valid():
            form.save()
            return redirect('myadmin_warehouse-flow_outbound')
    else:
        form =AddWarehouseInfoForm(instance=outbound)
    return render(request, 'myadmin/warehouse-flow/edit.html', {'form':form, 'id':id})


def delete_outbound(request, id):
    outbound = WmsOutbound.objects.get(pk=id)
    if request.method == "POST":
        outbound.delete()
        return redirect('myadmin_warehouse-flow_outbound')
    else:
        return render(request, 'myadmin/warehouse-flow/delete.html', {'outbound':outbound})
    

def add_to_inventory(item, quantity):
    # 入库逻辑
    pass

def remove_from_inventory(item, quantity):
    # 出库逻辑
    pass

def check_inventory(item):
    # 检查库存
    pass