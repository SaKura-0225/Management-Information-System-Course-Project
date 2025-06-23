from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from collections import defaultdict
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.decorators import permission_required, login_required

from myadmin.models import WmsOrders, WmsOrdersDetail
from .forms import AddOrdersInfoForm, OrderDetailForm
from myadmin.templatetags.auth_extras import multiple_permission_required
from django.utils import timezone
import qrcode
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


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
@multiple_permission_required(['myadmin.view_wmsorders', 'myadmin.view_wmsordersdetail'])
def wms_orders_detail(request, orders_id):
    order = get_object_or_404(WmsOrders, orders_id=orders_id)
    order_details = WmsOrdersDetail.objects.filter(orders__orders_id=orders_id)

    return render(request, "myadmin/orders/order_details.html", {
        "order": order,
        "wms_orders_details": order_details
    })


@login_required
@permission_required('myadmin.change_wmsorders', raise_exception=True)
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
@permission_required('myadmin.change_wmsorders', raise_exception=True)
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
@permission_required('myadmin.change_wmsorders', raise_exception=True)
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
@permission_required('myadmin.change_wmsorders', raise_exception=True)
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
@permission_required('myadmin.change_wmsorders', raise_exception=True)
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
@permission_required('myadmin.change_wmsorders', raise_exception=True)
def order_detail_delete(request, detail_id):
    detail = get_object_or_404(WmsOrdersDetail, pk=detail_id)
    if request.method == 'POST':
        detail.delete()
        return redirect('myadmin_order_detail_view')
    return render(request, 'myadmin/orders/detail_delete.html', {'detail': detail})



# 生成拣货单条码
def generate_order_barcode(order):
    import qrcode
    import os
    from django.conf import settings

    # 拣货员编号列表（过滤空值）
    pickers = [p.work_no for p in [order.work_no1, order.work_no2, order.work_no3,
                                   order.work_no4, order.work_no5, order.work_no6] if p]

    # 拼接二维码内容
    content = (
        f"orders_id:{order.orders_id} | "
        f"customer:{order.customer_id} | "
        f"create_at:{order.create_at.strftime('%Y-%m-%d %H:%M')} | "
        f"emergency:{order.emergency_status or '-'} | "
        f"status:{order.status or '-'} | "
        f"payment_status:{order.payment_status or '-'} | "
        f"total_amount:{order.total_amount or 0} | "
        f"pickers:{','.join(pickers)}"
    )

    # 保存路径设置
    folder = os.path.join(settings.BASE_DIR, 'static', 'barcodes', 'orders')
    os.makedirs(folder, exist_ok=True)

    filename = f"{order.orders_id}.png"
    path = os.path.join(folder, filename)

    # 生成二维码
    img = qrcode.make(content)
    img.save(path)

    return f"/static/barcodes/orders/{filename}", path



@login_required
@permission_required('myadmin.view_wmsorders', raise_exception=True)
def print_pick_list(request, orders_id):
    order = get_object_or_404(WmsOrders, orders_id=orders_id)
    details = WmsOrdersDetail.objects.filter(orders=order).select_related(
        'product__fabric_type', 'product__color', 'product__loc'
    )

    for d in details:
        d.subtotal = (d.quantity or 0) * (d.price or 0)

    pickers = [p for p in [
        order.work_no1, order.work_no2, order.work_no3,
        order.work_no4, order.work_no5, order.work_no6
    ] if p]

    total_qty = sum(d.quantity or 0 for d in details)
    total_money = sum(d.subtotal for d in details)

    barcode_url, barcode_path = generate_order_barcode(order)


    return render(request, 'myadmin/orders/print_pick_list.html', {
        'order': order,
        'pickers': pickers,
        'details': details,
        'total_qty': total_qty,
        'total_money': total_money,
        'print_time': timezone.now(),
        'barcode_url': barcode_url,
        'barcode_path': barcode_path,
    })


@csrf_exempt
def delete_barcode(request):
    if request.method == "POST":
        data = json.loads(request.body)
        path = data.get('path')
        if path and os.path.exists(path):
            os.remove(path)
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "fail"})