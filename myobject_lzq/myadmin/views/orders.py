from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from collections import defaultdict
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.decorators import permission_required, login_required

from myadmin.models import WmsOrders, WmsOrdersDetail
from .forms import AddOrdersInfoForm, OrderDetailForm

@login_required
@permission_required('myadmin.view_wmsorders', raise_exception=True)
def index(request):
    order_list = WmsOrders.objects.all().order_by("orders_id")
    
    # 查询过滤
    kw = request.GET.get("keyword")
    if kw:
        order_list = order_list.filter(
            Q(orders_id__icontains=kw) |
            Q(work_no1__work_no__icontains=kw) |
            Q(work_no2__work_no__icontains=kw) |
            Q(work_no3__work_no__icontains=kw) |
            Q(work_no4__work_no__icontains=kw) |
            Q(work_no5__work_no__icontains=kw) |
            Q(work_no6__work_no__icontains=kw)
        )
    
    # 筛选：拣货状态
    status = request.GET.get("status")
    if status in ['1', '2']:
        order_list = order_list.filter(status=status)

    # 筛选：紧急程度
    urgency = request.GET.get("urgency")
    if urgency in ['1', '2', '3']:
        order_list = order_list.filter(emergency_status=urgency)

    paginator = Paginator(order_list, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "myadmin/orders/index.html", {
        "orders_list": page_obj.object_list,
        "page_obj": page_obj,
        "filter_status": status,
        "filter_urgency": urgency,
    })


@login_required
@permission_required('myadmin.view_wmsorders', raise_exception=True)
def wms_orders_detail(request, orders_id):
    order = get_object_or_404(WmsOrders, orders_id=orders_id)
    order_details = WmsOrdersDetail.objects.filter(orders__orders_id=orders_id)

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
        form = AddOrdersInfoForm()
    return render(request, 'myadmin/orders/add.html', {'form': form})


@login_required
@permission_required('myadmin.view_wmsorders', raise_exception=True)
def edit_orders(request, orders_id):
    order = get_object_or_404(WmsOrders, orders_id=orders_id)
    if request.method == "POST":
        form = AddOrdersInfoForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('myadmin_order_index')
    else:
        form = AddOrdersInfoForm(instance=order)
    return render(request, 'myadmin/orders/edit.html', {
        'form': form,
        'orders_id': orders_id
    })


@login_required
@permission_required('myadmin.view_wmsorders', raise_exception=True)
def delete_orders(request, orders_id):
    order = get_object_or_404(WmsOrders, orders_id=orders_id)
    if request.method == "POST":
        order.delete()
        return redirect('myadmin_order_index')
    return render(request, 'myadmin/orders/delete.html', {'order': order})


@login_required
@permission_required('myadmin.view_wmsorders', raise_exception=True)
def order_detail_view(request):
    keyword = request.GET.get('keyword', '').strip()
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    filters = Q()
    if keyword:
        filters &= Q(orders__orders_id__icontains=keyword)

    try:
        if year and year.isdigit():
            year = int(year)
            if month and month.isdigit():
                month = int(month)
                if day and day.isdigit():
                    day = int(day)
                    start_date = datetime(year, month, day)
                    end_date = start_date + timedelta(days=1)
                else:
                    start_date = datetime(year, month, 1)
                    end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
            else:
                start_date = datetime(year, 1, 1)
                end_date = datetime(year + 1, 1, 1)

            filters &= Q(orders__create_at__gte=start_date, orders__create_at__lt=end_date)
    except ValueError:
        pass

    # 先查所有明细（可关联到 orders）
    all_details = WmsOrdersDetail.objects.select_related('orders').filter(filters)

    # 获取唯一订单编号列表（最新订单在前）
    all_orders = sorted(
        {d.orders for d in all_details},
        key=lambda o: o.create_at or datetime.min,
        reverse=True
    )

    # 分页（每页 20 个订单）
    paginator = Paginator(all_orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 从当前页的订单提取出明细并按订单号分组
    grouped = defaultdict(list)
    current_order_ids = [o.orders_id for o in page_obj]

    for detail in all_details:
        if detail.orders.orders_id in current_order_ids:
            grouped[detail.orders.orders_id].append(detail)

    return render(request, 'myadmin/orders/order_detail_view.html', {
        'grouped': dict(grouped),
        'keyword': keyword,
        'year': year,
        'month': month,
        'day': day,
        'page_obj': page_obj,
    })

@login_required
@permission_required('myadmin.view_wmsorders', raise_exception=True)
def order_detail_add(request, orders_id):
    order = get_object_or_404(WmsOrders, orders_id=orders_id)
    if request.method == 'POST':
        form = OrderDetailForm(request.POST)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.orders = order
            detail.save()
            return redirect('myadmin_order_detail_view')
    else:
        form = OrderDetailForm()
    return render(request, 'myadmin/orders/detail_form.html', {'form': form, 'order': order})

@login_required
@permission_required('myadmin.view_wmsorders', raise_exception=True)
def order_detail_edit(request, detail_id):
    detail = get_object_or_404(WmsOrdersDetail, pk=detail_id)
    if request.method == 'POST':
        form = OrderDetailForm(request.POST, instance=detail)
        if form.is_valid():
            form.save()
            return redirect('myadmin_order_detail_view')
    else:
        form = OrderDetailForm(instance=detail)
    return render(request, 'myadmin/orders/detail_form.html', {'form': form, 'order': detail.orders})

@login_required
@permission_required('myadmin.view_wmsorders', raise_exception=True)
def order_detail_delete(request, detail_id):
    detail = get_object_or_404(WmsOrdersDetail, pk=detail_id)
    if request.method == 'POST':
        detail.delete()
        return redirect('myadmin_order_detail_view')
    return render(request, 'myadmin/orders/detail_delete.html', {'detail': detail})
