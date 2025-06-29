# 后台子路由文件
from django.urls import path
from django.contrib import admin
from myadmin.views import index
from myadmin.views import orders
from myadmin.views import report,warehouse,warehouse_flow,system,customer,product,inventory,profile

urlpatterns = [
    path('', index.index, name="myadmin_index"),  # 后台首页

    # 后台管理员登录、退出路由
    path('login', index.logins, name="myadmin_login"),  # 加载登录表单
    #path('dologin', index.dologin, name="myadmin_dologin"),  # 执行登录表单
    path('logout', index.logout, name="myadmin_logout"),  # 退出
    path('verify', index.verify, name="myadmin_verify"),  # 输出验证码
    # 会员管理路由

    # 订单信息管理路由
    path('orders/', orders.index, name="myadmin_order_index"),  # 浏览
    path('orders/<int:orders_id>', orders.wms_orders_detail, name='myadmin_orders_detail'), #根据订单编号浏览订单详情
    path('orders/add', orders.add_orders, name='myadmin_orders_add'),  #增加新订单
    path('orders/<int:orders_id>/edit', orders.edit_orders, name='myadmin_orders_edit'),  #根据订单编号修改已有订单
    path('orders/<int:orders_id>/delete', orders.delete_orders, name='myadmin_orders_delete'), #根据订单编号删除订单
    path('orders/detail/', orders.order_detail_view, name='myadmin_order_detail_view'),
    path('orders/detail/add/<int:orders_id>/', orders.order_detail_add, name='myadmin_order_detail_add'),
    path('orders/detail/edit/<int:detail_id>/', orders.order_detail_edit, name='myadmin_order_detail_edit'),
    path('orders/detail/delete/<int:detail_id>/', orders.order_detail_delete, name='myadmin_order_detail_delete'),
    path('orders/<int:orders_id>/print/', orders.print_pick_list, name='myadmin_orders_print'), #打印拣货单
    path('orders/barcode/delete/', orders.delete_barcode, name='myadmin_delete_barcode'),#删除条形码




    #出入库管理路由
    path('warehouse-flow/inbound', warehouse_flow.inbound_index , name='myadmin_warehouse-flow_inbound'), #出库表单
    path('warehouse-flow/outbound', warehouse_flow.outbound_index , name='myadmin_warehouse-flow_outbound'), #入库表单
    path('warehouse-flow/outbound/add', warehouse_flow.add_outbound, name='myadmin_outbound_add'),  #增加新订单
    path('warehouse-flow/outbound/<int:id>/edit', warehouse_flow.edit_outbound, name='myadmin_outbound_edit'),  #根据订单编号修改已有订单
    path('warehouse-flow/outbound/<int:id>/delete', warehouse_flow.delete_outbound, name='myadmin_outbound_delete'), #根据订单编号删除订单

    #报表界面路由
    path('report', report.index, name='myadmin_report_index'), #主页浏览


    #仓位可视化路由
    path("warehouse", warehouse.bin_visualization, name="myadmin_bin_visualization"), #仓位可视化


    # 系统管理路由
    path('system/employee', system.employee_index, name='myadmin_system_employee_index'), #员工管理
    path('system/employee/add', system.add_employee, name='myadmin_system_employee_add'), #员工添加
    path('system/employee/<int:user_id>/edit', system.edit_employee, name='myadmin_system_employee_edit'), #员工编辑
    #path('system/employee/<int:id>/delete', system.employee_delete, name='myadmin_system_employee_delete'), #员工删除
    path('system/department', system.department_index, name='myadmin_system_department_index'), #部门管理
    #path('system/department/add', system.department_add, name='myadmin_system_department_add'), #部门添加
    #path('system/department/<int:id>/edit', system.department_edit, name='myadmin_system_department_edit'), #部门编辑
    #path('system/department/<int:id>/delete', system.department_delete, name='myadmin_system_department_delete'), #部门删除
    path('system/permission', system.permission_index, name='myadmin_system_permission_index'), #权限管理
    #path('system/permission/add', system.permission_add, name='myadmin_system_permission_add'), #权限添加       
    path('system/permission/<int:group_id>/edit', system.edit_permissions, name='myadmin_system_permission_edit'), #权限编辑
    #path('system/permission/<int:id>/delete', system.permission_delete, name='myadmin_system_permission_delete'), #权限删除

    # 客户管理路由
    path('customer', customer.index, name='myadmin_customer_index'), #客户管理
    path('customer/add', customer.add_customer, name='myadmin_customer_add'), #客户添加
    path('customer/<int:id>/edit', customer.edit_customer, name='myadmin_customer_edit'), #客户编辑
    path('customer/<int:id>/delete', customer.customer_delete, name='myadmin_customer_delete'), #客户删除

    #产品信息管理路由
    path('product', product.index, name='myadmin_product_index'), #产品信息管理
    path('product/add', product.add_product, name='myadmin_product_add'), #产品信息添加
    path('product/<int:id>/edit', product.edit_product, name='myadmin_product_edit'), #产品信息编辑
    path('product/<int:id>/delete', product.product_delete, name='myadmin_product_delete'), #产品信息删除


    # 库存信息路由
    path('inventory', inventory.stock_index, name='myadmin_stock_index'),
    path('inventory/<str:product_id>/check', inventory.check_inventory, name='myadmin_stock_check'),

    # 个人页面路由
    path('profile/', profile.my_profile, name='myadmin_profile'), #个人页面
]