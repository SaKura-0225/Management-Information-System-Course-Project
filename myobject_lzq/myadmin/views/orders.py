# 员工信息管理视图文件
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
# Create your views here.
from myadmin.models import WmsOrders,WmsOrdersDetail
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.db.models import Avg, Max, Min, Count, Sum
from .forms import AddOrdersInfoForm

def index(request):
    umod = WmsOrders.objects.all()
    order_list = umod.order_by("orders_id")  # 对id排序
    #查询
    kw = request.GET.get("keyword", None)
    if kw:
        order_list = order_list.filter(Q(num__contains=kw) | Q(id__contains=kw)) #根据视图中选取订单编号或者id查询
    paginator = Paginator(order_list, 4)  # Show 1 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # 显示所有数据代码：
    context = {"orders_list": order_list,"page_obj": page_obj}
    return render(request, "myadmin/orders/index.html", context)



def wms_orders_detail(request, orders_id):
    try:
        order = WmsOrders.objects.get(orders_id=orders_id)  
    except WmsOrders.DoesNotExist:
        return HttpResponse("订单不存在", status=404)

    order_details = WmsOrdersDetail.objects.filter(orders_id=orders_id)

    return render(request, "myadmin/orders/order_details.html", {
        "order": order,
        "wms_orders_details": order_details
    })


def add_orders(request):
    if request.method == "POST":
        form = AddOrdersInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("订单创建完成")
    else:
        form =AddOrdersInfoForm()
    return render(request, 'myadmin/orders/add.html', {'form':form})


def edit_orders(request, orders_id):
    order = WmsOrders.objects.get(orders_id=orders_id)
    if request.method == "POST":
        form = AddOrdersInfoForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('myadmin_order_index')
    else:
        form =AddOrdersInfoForm(instance=order)
    return render(request, 'myadmin/orders/edit.html', {'form':form, 'orders_id':orders_id})


def delete_orders(request, orders_id):
    order = WmsOrders.objects.get(orders_id=orders_id)
    if request.method == "POST":
        order.delete()
        return redirect('myadmin_order_index')
    else:
        return render(request, 'myadmin/orders/delete.html', {'order':order})