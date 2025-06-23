from django.shortcuts import render, get_object_or_404, redirect
from myadmin.models import WmsProduct, WmsBinStorage, WmsStockCheck
from .forms import StockCheckForm
from django.db.models import F, Sum, Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Max
from django.utils import timezone

# 库存总览 + 预警


@login_required
@permission_required('myadmin.view_wmsbinstorage', raise_exception=True)
def stock_index(request):
    search_pid = request.GET.get("product_id", "").strip()
    search_fabric = request.GET.get("fabric_type", "").strip()
    search_color = request.GET.get("color", "").strip()
    search_status = request.GET.get("status", "").strip()  # normal / warning

    # 获取所有原始库存记录
    stock_data = WmsBinStorage.objects.select_related('loc').values(
        'product_id', 'loc_id', 'quantity', 'min_threshold'
    )
    products = WmsProduct.objects.select_related('color', 'fabric_type').all()
    product_dict = {p.product_id: p for p in products}

    # ✅ 解决 MySQL 不支持 distinct on 的问题：分步获取每个产品最新盘点记录
    latest_check_times = (
        WmsStockCheck.objects
        .values('product_id')
        .annotate(latest_time=Max('check_time'))
    )

    stock_check_map = {}
    for entry in latest_check_times:
        product_id = entry['product_id']
        latest = WmsStockCheck.objects.filter(
            product_id=product_id,
            check_time=entry['latest_time']
        ).first()
        if latest:
            stock_check_map[product_id] = latest.actual_qty

    # 构造最终展示数据
    overview = []
    for s in stock_data:
        product = product_dict.get(s['product_id'])
        if not product:
            continue

        # ✅ 使用最新盘点值（如果有）作为显示库存
        latest_qty = stock_check_map.get(s['product_id'], s['quantity'])
        is_warning = latest_qty < s['min_threshold']

        # 搜索过滤逻辑
        if search_pid and search_pid not in product.product_id:
            continue
        if search_fabric and (not product.fabric_type or search_fabric not in product.fabric_type.fabric_type_name):
            continue
        if search_color and (not product.color or search_color not in product.color.color_name):
            continue
        if search_status:
            if search_status == "warning" and not is_warning:
                continue
            if search_status == "normal" and is_warning:
                continue

        overview.append({
            'product': product,
            'loc_id': s['loc_id'],
            'quantity': latest_qty,
            'threshold': s['min_threshold'],
            'is_warning': is_warning
        })

    overview.sort(key=lambda x: x['quantity'])

    paginator = Paginator(overview, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "myadmin/inventory/index.html", {
        'page_obj': page_obj,
        'search_pid': search_pid,
        'search_fabric': search_fabric,
        'search_color': search_color,
        'search_status': search_status,
    })

# 发起盘点
@login_required
@permission_required('myadmin.view_wmsbinstorage', raise_exception=True)
def check_inventory(request, product_id):
    product = get_object_or_404(WmsProduct, product_id=product_id)
    loc = WmsBinStorage.objects.filter(product_id=product_id).first()
    expected_qty = loc.quantity if loc else 0

    if request.method == "POST":
        form = StockCheckForm(request.POST)
        if form.is_valid():
            check = form.save(commit=False)
            check.product = product
            check.expected_qty = expected_qty  # ✅ 显式赋值
            check.check_time = timezone.now()  # ✅ 保证写入时间
            check.checked_by = request.user.username  # ✅ 保证写入检查人
            check.save()
            return redirect('myadmin_stock_index')
    else:
        form = StockCheckForm(initial={
            'checked_by': request.user.username
        })

    return render(request, "myadmin/inventory/check_form.html", {
        'form': form,
        'product': product,
        'expected_qty': expected_qty
    })
