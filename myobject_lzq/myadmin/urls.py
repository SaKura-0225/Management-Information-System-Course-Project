# 后台子路由文件
from django.urls import path
from django.contrib import admin
from myadmin.views import index
from myadmin.views import user
from myadmin.views import shop
from myadmin.views import orders
from myadmin.views import category, product, member
from myadmin.views import report,warehouse,warehouse_flow

urlpatterns = [
    path('', index.index, name="myadmin_index"),  # 后台首页

    # 后台管理员登录、退出路由
    path('login', index.logins, name="myadmin_login"),  # 加载登录表单
    #path('dologin', index.dologin, name="myadmin_dologin"),  # 执行登录表单
    path('logout', index.logout, name="myadmin_logout"),  # 退出
    path('verify', index.verify, name="myadmin_verify"),  # 输出验证码

    # 店铺信息管理路由
    path('shop/', shop.index, name="myadmin_shop_index"),  # 浏览
    path('shop/add', shop.add, name="myadmin_shop_add"),  # 添加表单
    path('shop/insert', shop.insert, name="myadmin_shop_insert"),  # 执行添加
    path('shop/del/<int:sid>', shop.delete, name="myadmin_shop_delete"),  # 执行删除
    path('shop/edit/<int:sid>', shop.edit, name="myadmin_shop_edit"),  # 加载编辑表单
    path('shop/update/<int:sid>', shop.update, name="myadmin_shop_update"),  # 执行编辑

    # 员工信息管理路由
    path('user/', user.index, name="myadmin_user_index"),  # 浏览
    path('user/add', user.add, name="myadmin_user_add"),  # 添加表单
    path('user/insert', user.insert, name="myadmin_user_insert"),  # 执行添加
    path('user/del/<int:uid>', user.delete, name="myadmin_user_delete"),  # 执行删除
    path('user/edit/<int:uid>', user.edit, name="myadmin_user_edit"),  # 加载编辑表单
    path('user/update/<int:uid>', user.update, name="myadmin_user_update"),  # 执行编辑

    # 菜品分类信息管理路由
    path('category/', category.index, name="myadmin_category_index"),  # 浏览
    path('category/load/<int:sid>', category.loadCategory, name="myadmin_category_load"),
    path('category/add', category.add, name="myadmin_category_add"),  # 添加表单
    path('category/insert', category.insert, name="myadmin_category_insert"),  # 执行添加
    path('category/del/<int:cid>', category.delete, name="myadmin_category_del"),  # 执行删除
    path('category/edit/<int:cid>', category.edit, name="myadmin_category_edit"),  # 加载编辑表单
    path('category/update/<int:cid>', category.update, name="myadmin_category_update"),  # 执行编辑

    # 菜品信息管理路由
    path('product/', product.index, name="myadmin_product_index"),  # 浏览
    path('product/add', product.add, name="myadmin_product_add"),  # 添加表单
    path('product/insert', product.insert, name="myadmin_product_insert"),  # 执行添加
    path('product/del/<int:pid>', product.delete, name="myadmin_product_del"),  # 执行删除
    path('product/edit/<int:pid>', product.edit, name="myadmin_product_edit"),  # 加载编辑表单
    path('product/update/<int:pid>', product.update, name="myadmin_product_update"),  # 执行编辑

    # 会员管理路由
    path('member/', member.index, name="myadmin_member_index"),  # 浏览会员信息
    path('member/del/<int:mid>', member.delete, name="myadmin_member_del"),  # 执行删除

    # 订单信息管理路由
    path('orders/', orders.index, name="myadmin_order_index"),  # 浏览
    path('orders/<int:orders_id>', orders.wms_orders_detail, name='myadmin_orders_detail'), #根据订单编号浏览订单详情
    path('orders/add', orders.add_orders, name='myadmin_orders_add'),  #增加新订单
    path('orders/<int:orders_id>/edit', orders.edit_orders, name='myadmin_orders_edit'),  #根据订单编号修改已有订单
    path('orders/<int:orders_id>/delete', orders.delete_orders, name='myadmin_orders_delete'), #根据订单编号删除订单
    path('orders/detail/', orders.order_detail_view, name='myadmin_order_detail_view'),


    #出入库管理路由
    path('warehouse-flow/inbound', warehouse_flow.inbound_index , name='myadmin_warehouse-flow_inbound'), #出库表单
    path('warehouse-flow/outbound', warehouse_flow.outbound_index , name='myadmin_warehouse-flow_outbound'), #入库表单
    path('warehouse-flow/outbound/add', warehouse_flow.add_outbound, name='myadmin_outbound_add'),  #增加新订单
    path('warehouse-flow/outbound/<int:id>/edit', warehouse_flow.edit_outbound, name='myadmin_outbound_edit'),  #根据订单编号修改已有订单
    path('warehouse-flow/outbound/<int:id>/delete', warehouse_flow.delete_outbound, name='myadmin_outbound_delete'), #根据订单编号删除订单

    #报表界面路由
    path('report', report.index, name='myadmin_report_index'), #主页浏览


    #仓位可视化路由
    path('warehouse', warehouse.index, name='myadmin_warehouse_index'), #主页浏览
]


