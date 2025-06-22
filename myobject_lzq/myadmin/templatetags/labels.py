from django import template

register = template.Library()

PERM_LABELS = {   
    # 以下为你贴出的真实 model 权限
    'view_myadmindepartment': '查看部门',
    'view_myadminemployeeprofile': '查看员工档案',
    'view_wmsbinstorage': '查看库存',
    'view_wmscustomer': '查看客户信息',
    'view_wmsorders': '查看销售订单',
    'view_wmsordersdetail': '查看订单明细',
    'view_wmsoutbound': '查看出库记录',
    'view_wmsproduct': '查看商品',
    'view_wmsproductcolor': '查看商品颜色',
    'view_wmsproductfabrictype': '查看商品布料类型',
    'view_wmsstockcheck': '查看库存盘点',
}

@register.filter
def perm_label(codename):
    return PERM_LABELS.get(codename, codename)
