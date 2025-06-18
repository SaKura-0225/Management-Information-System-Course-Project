
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from myadmin.models import Department, EmployeeProfile

class Command(BaseCommand):
    help = '导入初始员工和权限组'

    def handle(self, *args, **options):
        # 创建部门
        sales = Department.objects.get_or_create(name='销售部', code='sales')[0]
        warehouse = Department.objects.get_or_create(name='仓储部', code='warehouse')[0]

        # 创建权限组
        g_sales = Group.objects.get_or_create(name='销售权限')[0]
        g_warehouse = Group.objects.get_or_create(name='仓储权限')[0]

        # 创建用户
        u1 = User.objects.create_user(username='alice', password='123456')
        EmployeeProfile.objects.create(user=u1, department=sales, work_no='S001')
        u1.groups.add(g_sales)

        u2 = User.objects.create_user(username='bob', password='123456')
        EmployeeProfile.objects.create(user=u2, department=warehouse, work_no='W001')
        u2.groups.add(g_warehouse)

        self.stdout.write(self.style.SUCCESS('初始化用户和权限组成功'))
