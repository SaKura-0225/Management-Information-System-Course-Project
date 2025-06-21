
#报表管理视图文件
from django.db.models import Sum, Count
from django.shortcuts import render
from myadmin.models import WmsOrders, WmsOrdersDetail
from datetime import datetime, timedelta

def index(request):
    raw_data = (
        WmsOrders.objects
        .extra({'date': "DATE(create_at)"})
        .values('date')
        .annotate(order_count=Count('orders_id'), total_qty=Sum('total_amount'))
        .order_by('date')
    )

    dates = [str(row['date']) for row in raw_data]
    counts = [row['order_count'] for row in raw_data]

    return render(request, 'myadmin/report/index.html', {
        'dates': dates,
        'counts': counts
    })

