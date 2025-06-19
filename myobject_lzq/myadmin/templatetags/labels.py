from django import template

register = template.Library()

PERM_LABELS = {
    'view_category': '查看分类',
    'view_department': '查看部门',
    'view_employeeprofile': '查看员工档案',
    'view_member': '查看会员',
    'view_order2': '查看订单2',
    'view_orders': '查看订单',
    'view_ordersdetailwithdates': '查看订单明细',
    'view_product': '查看商品',
    'view_shop': '查看门店',
    'view_wmsorders': '查看销售订单',
    'view_wmsoutbound': '查看出库记录',
}

@register.filter
def perm_label(codename):
    return PERM_LABELS.get(codename, codename)
