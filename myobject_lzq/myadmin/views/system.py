
# 系统管理视图文件
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group, Permission
from myadmin.models import Department, EmployeeProfile
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from myadmin.models import EmployeeProfile
from django.contrib.contenttypes.models import ContentType
from .forms import UserForm, EmployeeForm


# 部门编码 → 权限组映射
DEPARTMENT_GROUP_MAP = {
    'sales': '销售权限',
    'warehouse': '仓储权限',
    'buy': '采购权限',
    'human_resources': '人事权限',
    'produce': '生产权限',
}

@login_required
@permission_required('myadmin.view_myadminemployeeprofile', raise_exception=True)
def employee_index(request):
    employees = EmployeeProfile.objects.select_related('user', 'department').all()
    return render(request, 'myadmin/system/employees/index.html', {'employees': employees})


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            profile = form.save()

            # 自动为对应用户添加权限组
            try:
                department = profile.department
                if department:
                    group_name = DEPARTMENT_GROUP_MAP.get(department.code)
                    if group_name:
                        group = Group.objects.get(name=group_name)
                        user = User.objects.get(id=profile.user_id)
                        user.groups.clear()  # 清除旧的组（可选）
                        user.groups.add(group)
            except Exception as e:
                print("自动添加权限失败：", e)

            return redirect('myadmin_system_employee_index')
    else:
        form = EmployeeForm()

    return render(request, 'myadmin/system/employees/add.html', {'form': form})
@login_required
@permission_required('myadmin.view_myadminemployeeprofile', raise_exception=True)
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
@permission_required('myadmin.view_myadmindepartment', raise_exception=True)
def department_index(request):
    departments = Department.objects.prefetch_related('employeeprofile_set__user').all()
    return render(request, 'myadmin/system/department/index.html', {'departments': departments})


@login_required
@permission_required('auth.is_supervisor', raise_exception=True)
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

@login_required
@permission_required('auth.is_supervisor', raise_exception=True)
def edit_permissions(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    myadmin_perms = Permission.objects.filter(content_type__app_label='myadmin', codename__startswith='view_')

    if request.method == 'POST':
        selected = request.POST.getlist('permissions')  # 获取提交的权限 ID 列表
        group.permissions.set(selected)  # 更新权限组的权限
        return redirect('myadmin_system_permission_index')  # 重定向回权限首页

    current_permissions = group.permissions.values_list('id', flat=True)

    return render(request, 'myadmin/system/permission/edit.html', {
        'group': group,
        'permissions': myadmin_perms,
        'current_permissions': current_permissions
    })
