<<<<<<< HEAD

# 系统管理视图文件
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group, Permission
from myadmin.models import Department, EmployeeProfile
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from myadmin.models import EmployeeProfile
from django.contrib.contenttypes.models import ContentType
from .forms import UserForm, EmployeeForm


@login_required
@permission_required('auth.view_user', raise_exception=True)
def employee_index(request):
    employees = EmployeeProfile.objects.select_related('user', 'department').all()
    return render(request, 'myadmin/system/employees/index.html', {'employees': employees})

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myadmin_system_employee_index')  
    else:
        form = EmployeeForm()
    return render(request, 'myadmin/system/employees/add.html', {'form': form})


def edit_employee(request, user_id):
    employee = get_object_or_404(EmployeeProfile, user__id=user_id)
    user = employee.user

    if request.method == 'POST':
        uform = UserForm(request.POST, instance=user)
        eform = EmployeeForm(request.POST, instance=employee)
        if uform.is_valid() and eform.is_valid():
            u = uform.save(commit=False)
            pwd = uform.cleaned_data.get('password')
            if pwd:
                u.set_password(pwd)
            u.save()
            u.groups.set(uform.cleaned_data['groups'])  # 更新权限组
            eform.save()
            return redirect('myadmin_system_employee_index')
    else:
        uform = UserForm(instance=user)
        eform = EmployeeForm(instance=employee)

    return render(request, 'myadmin/system/employees/edit.html', {
        'uform': uform,
        'eform': eform
    })

@login_required
@permission_required('myadmin.view_department', raise_exception=True)
def department_index(request):
    departments = Department.objects.prefetch_related('employeeprofile_set__user').all()
    return render(request, 'myadmin/system/department/index.html', {'departments': departments})


@login_required
@permission_required('auth.view_group', raise_exception=True)
def permission_index(request):
    myadmin_ct = ContentType.objects.filter(app_label='myadmin')
    groups = Group.objects.all().prefetch_related('permissions')

    # 筛选每个组只保留 myadmin 权限
    group_data = []
    for g in groups:
        perms = g.permissions.filter(content_type__in=myadmin_ct)
        group_data.append({
            'group': g,
            'permissions': perms,
        })

    return render(request, 'myadmin/system/permission/index.html', {
        'groups': group_data
    })

def edit_permissions(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    myadmin_perms = Permission.objects.filter(content_type__app_label='myadmin', codename__startswith='view_')

    if request.method == 'POST':
        selected = request.POST.getlist('permissions')  # 获取提交的权限 ID 列表
        group.permissions.set(selected)  # 更新权限组的权限
        return redirect('myadmin_permission_index')  # 重定向回权限首页

    current_permissions = group.permissions.values_list('id', flat=True)

    return render(request, 'myadmin/system/permission/edit.html', {
        'group': group,
        'permissions': myadmin_perms,
        'current_permissions': current_permissions
    })
=======
# 系统管理视图文件
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from collections import defaultdict
from datetime import datetime, timedelta
# Create your views here.
from myadmin.models import 
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.db.models import Avg, Max, Min, Count, Sum
from .forms import 
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
>>>>>>> f7fabbd (消除原始代码影响1)
