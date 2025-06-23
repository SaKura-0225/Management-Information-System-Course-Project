from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from myadmin.models import EmployeeProfile, WmsOrders

@login_required
def my_profile(request):
    user = request.user
    try:
        employee = EmployeeProfile.objects.select_related('department').get(user=user)
        work_no = employee.work_no
    except EmployeeProfile.DoesNotExist:
        employee = None
        work_no = None

    # 查询当前拣货员关联的未拣货订单
    picking_tasks = []
    if work_no:
        picking_tasks = WmsOrders.objects.filter(
            Q(work_no1=work_no) |
            Q(work_no2=work_no) |
            Q(work_no3=work_no) |
            Q(work_no4=work_no) |
            Q(work_no5=work_no) |
            Q(work_no6=work_no),
            status=2,  # 未拣货
        ).select_related('customer').order_by('-create_at')

    return render(request, 'myadmin/profile/index.html', {
        'user': user,
        'employee': employee,
        'picking_tasks': picking_tasks,
    })
