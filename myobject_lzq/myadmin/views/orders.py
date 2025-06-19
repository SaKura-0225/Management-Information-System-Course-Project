# 订单信息管理视图文件
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from collections import defaultdict
from datetime import datetime, timedelta
# Create your views here.
from myadmin.models import WmsOrders,OrdersDetailWithDates
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.db.models import Avg, Max, Min, Count, Sum
from .forms import AddOrdersInfoForm
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.contrib.auth.decorators import permission_required

@permission_required('myadmin.view_wmsorders', raise_exception=True)
def index(request):
    umod = WmsOrders.objects.all()
    order_list = umod.order_by("orders_id")  # 对id排序
    #查询
    kw = request.GET.get("keyword", None)
    if kw:
        order_list = order_list.filter(Q(orders_id__contains=kw)) #根据视图中选取订单编号查询
    paginator = Paginator(order_list, 4)  
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

    order_details = OrdersDetailWithDates.objects.filter(orders_id=orders_id)

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
    

def order_detail_view(request):
    # 获取搜索参数
    keyword = request.GET.get('keyword', '').strip()
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    # 初始查询集
    details = OrdersDetailWithDates.objects.all()

    # 构建过滤条件
    filters = Q()

    if keyword:
        filters &= Q(orders_id__icontains=keyword)

    # 时间范围构建（只使用 >= 和 < 避免时区问题）
    try:
        if year and year.isdigit():
            year = int(year)
            if month and month.isdigit():
                month = int(month)
                if day and day.isdigit():
                    day = int(day)
                    # 指定到某一天
                    start_date = datetime(year, month, day)
                    end_date = start_date + timedelta(days=1)
                else:
                    # 指定到某一月
                    start_date = datetime(year, month, 1)
                    if month == 12:
                        end_date = datetime(year + 1, 1, 1)
                    else:
                        end_date = datetime(year, month + 1, 1)
            else:
                # 仅年
                start_date = datetime(year, 1, 1)
                end_date = datetime(year + 1, 1, 1)

            filters &= Q(create_at__gte=start_date, create_at__lt=end_date)

    except ValueError:
        pass  # 忽略非法日期

    # 应用过滤条件
    details = details.filter(filters).order_by('orders_id')
    # 分组聚合
    grouped = defaultdict(list)
    for row in details:
        grouped[row.orders_id].append(row)

    return render(request, 'myadmin/orders/order_detail_view.html', {
        'grouped': dict(grouped),
        'keyword': keyword,
        'year': year,
        'month': month,
        'day': day,
    })