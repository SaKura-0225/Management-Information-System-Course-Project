from django.db.models import Sum, Count
from django.shortcuts import render
from myadmin.models import WmsOrders, WmsOrdersDetail, WmsProduct, WmsCustomer
from collections import defaultdict
from django.db.models.functions import TruncMonth

def index(request):
    selected_charts = request.GET.getlist('charts')
    show_all = not selected_charts
    selected_charts = selected_charts or ['daily_orders', 'top_products', 'monthly_top_products', 'customer_levels','monthly_top_products1']
    

    # 图表1：每日订单趋势
    daily_data = (
        WmsOrders.objects
        .extra({'date': "DATE(create_at)"})
        .values('date')
        .annotate(order_count=Count('orders_id'), total_qty=Sum('total_amount'))
        .order_by('date')
    )
    daily_chart = {
        'dates': [str(row['date']) for row in daily_data],
        'counts': [row['order_count'] for row in daily_data]
    }

    # 图表2：出货前十型号
    top_raw = (
        WmsOrdersDetail.objects
        .values('product_id')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:10]
    )

    # 图表3：客户等级分布
    level_chart_data = []
    if show_all or 'customer_levels' in selected_charts:
        level_map = {
            1: '一级客户',
            2: '二级客户',
            3: '三级客户',
            4: '四级客户',
            5: '五级客户',
        }
        level_counts = (
            WmsCustomer.objects
            .values('level')
            .annotate(count=Count('id'))
            .order_by('level')
        )

        level_chart_data = [
            {
                'name': level_map.get(row['level'], f'等级{row["level"]}'),
                'value': row['count']
            }
            for row in level_counts if row['level'] is not None
        ]

    # 图表4：支持筛选的月份前十出货产品
    monthly_grouped_data = defaultdict(list)
    if show_all or 'monthly_top_products1' in selected_charts:
        monthly_data = (
            WmsOrdersDetail.objects
            .extra(select={'month': "DATE_FORMAT(wms_orders_detail.create_at, '%%Y-%%m')"})
            .values('month', 'product_id')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('month', '-total_quantity')
        )

        # 构建产品名映射
        product_map = {
            p.product_id: f"{p.fabric_type.fabric_type_name} - {p.color.color_name}"
            for p in WmsProduct.objects.select_related('fabric_type', 'color')
            if p.fabric_type and p.color
        }

        for row in monthly_data:
            month = row['month']
            if len(monthly_grouped_data[month]) < 10:
                prod_name = product_map.get(row['product_id'], row['product_id'])
                monthly_grouped_data[month].append({
                    'name': prod_name,
                    'value': row['total_quantity']
                })

        monthly_chart_map = dict(monthly_grouped_data)
        all_months = sorted(monthly_chart_map.keys(), reverse=True)
    else:
        monthly_chart_map = {}
        all_months = []

    # 关联产品名称
    products = WmsProduct.objects.select_related('fabric_type', 'color')
    product_map = {
        p.product_id: f"{p.fabric_type.fabric_type_name} - {p.color.color_name}"
        for p in products if p.fabric_type and p.color
    }

    top_chart_labels = [
        product_map.get(row['product_id'], row['product_id']) for row in top_raw
    ]
    top_chart_values = [row['total_quantity'] for row in top_raw]

    return render(request, 'myadmin/report/index.html', {
        'selected_charts': selected_charts,
        'show_all': show_all,
        'daily_chart': daily_chart,
        'top_chart_labels': top_chart_labels,
        'top_chart_values': top_chart_values,
        'level_chart_data': level_chart_data,
        'monthly_chart_map': dict(monthly_chart_map),
        'all_months': all_months,
    })

