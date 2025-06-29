
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.

#布料销售订单
class WmsOrders(models.Model):
    orders_id = models.IntegerField(primary_key=True, db_comment='订单编号')
    total_amount = models.IntegerField(blank=True, null=True, db_comment='面料出库总量')
    category = models.IntegerField(blank=True, null=True, db_comment='1：镇内订单  2：镇外订单')
    payment_status = models.IntegerField(blank=True, null=True, db_comment='财务状态:1未到账/2已到账')
    customer = models.ForeignKey('WmsCustomer', models.DO_NOTHING, to_field='customers_id', blank=True, null=True, db_comment='采购企业代号')
    work_no1 = models.ForeignKey('MyadminEmployeeprofile', models.DO_NOTHING, db_column='work_no1', to_field='work_no', blank=True, null=True, db_comment='拣货员工号1')
    work_no2 = models.ForeignKey('MyadminEmployeeprofile', models.DO_NOTHING, db_column='work_no2', to_field='work_no', related_name='wmsorders_work_no2_set', blank=True, null=True, db_comment='拣货员工号2')
    work_no3 = models.ForeignKey('MyadminEmployeeprofile', models.DO_NOTHING, db_column='work_no3', to_field='work_no', related_name='wmsorders_work_no3_set', blank=True, null=True, db_comment='拣货员工号3')
    work_no4 = models.ForeignKey('MyadminEmployeeprofile', models.DO_NOTHING, db_column='work_no4', to_field='work_no', related_name='wmsorders_work_no4_set', blank=True, null=True, db_comment='拣货员工号4')
    work_no5 = models.ForeignKey('MyadminEmployeeprofile', models.DO_NOTHING, db_column='work_no5', to_field='work_no', related_name='wmsorders_work_no5_set', blank=True, null=True, db_comment='拣货员工号5')
    work_no6 = models.ForeignKey('MyadminEmployeeprofile', models.DO_NOTHING, db_column='work_no6', to_field='work_no', related_name='wmsorders_work_no6_set', blank=True, null=True, db_comment='拣货员工号6')
    emergency_status = models.IntegerField(blank=True, null=True, db_comment='紧急程度1正常2加急3紧急')
    status = models.IntegerField(blank=True, null=True, db_comment='1:已拣货  2:未拣货')
    qrcode = models.CharField(max_length=100, blank=True, null=True, db_comment='拣货单二维码')
    create_at = models.DateTimeField(blank=True, null=True, db_comment='下单时间')
    update_at = models.DateTimeField(blank=True, null=True, db_comment='更新时间')

    def __str__(self):
        return f"订单 #{self.orders_id} - 客户: {self.customer.company_name if self.customer else '未知'}"
    class Meta:
        managed = True
        db_table = 'wms_orders'
        db_table_comment = '销售订单表'

#布料销售订单详情
class WmsOrdersDetail(models.Model):
    orders = models.ForeignKey('WmsOrders', models.DO_NOTHING, db_comment='订单编号')
    product = models.ForeignKey('WmsProduct', models.DO_NOTHING, to_field='product_id', blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True, db_comment='单价')
    total_price = models.FloatField(blank=True, null=True)
    create_at = models.DateTimeField(blank=True, null=True, db_comment='下单日期')

    class Meta:
        managed = True
        db_table = 'wms_orders_detail'

#出库表
class WmsOutbound(models.Model):
    orders = models.ForeignKey('WmsOrders', models.DO_NOTHING, blank=True, null=True, db_comment='销售订单id')
    product = models.ForeignKey('WmsProduct', models.DO_NOTHING, to_field='product_id', blank=True, null=True, db_comment='SKU编号')
    quantity = models.IntegerField(blank=True, null=True, db_comment='数量')
    loc = models.ForeignKey('WmsBinStorage', models.DO_NOTHING, to_field='loc_id', blank=True, null=True, db_comment='库位编号')
    work_no = models.ForeignKey('MyadminEmployeeprofile', models.DO_NOTHING, db_column='work_no', to_field='work_no', blank=True, null=True, db_comment='操作员工号')
    create_at = models.DateTimeField(blank=True, null=True, db_comment='出库时间')
    update_at = models.DateTimeField(blank=True, null=True, db_comment='更新时间')

    def __str__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'wms_outbound'
        db_table_comment = '出库表'


# 部门表
class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        managed = False

class MyadminDepartment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    code = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = True
        db_table = 'myadmin_department'

        

# 员工扩展信息（绑定用户）

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_constraint=False)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    work_no = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.IntegerField(blank=True, null=True, db_comment='性别 男1/女2')

    def __str__(self):
        return self.user.username
    class Meta:
        managed = False
        
class MyadminEmployeeprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    work_no = models.CharField(unique=True, max_length=100)
    gender = models.IntegerField(blank=True, null=True, db_comment='性别 男1/女2')
    phone = models.CharField(max_length=20)
    department = models.ForeignKey('MyadminDepartment', models.DO_NOTHING, blank=True, null=True)
    user_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.work_no
    class Meta:
        managed = True
        db_table = 'myadmin_employeeprofile'
    
# 产品信息表
class WmsProduct(models.Model):
    product_id = models.CharField(unique=True, max_length=10, blank=True, null=True, db_comment='产品编号')
    fabric_type = models.ForeignKey('WmsProductFabricType', models.DO_NOTHING, to_field='fabric_type_id', blank=True, null=True, db_comment='布料品种id')
    color = models.ForeignKey('WmsProductColor', models.DO_NOTHING, to_field='color_id', blank=True, null=True, db_comment='布料颜色id')
    loc = models.ForeignKey('WmsBinStorage', models.DO_NOTHING, to_field='loc_id', blank=True, null=True, db_comment='库位编码')
    price = models.IntegerField(blank=True, null=True, db_comment='单价')
    barcode_file = models.CharField(max_length=100, blank=True, null=True, db_comment='条码图片文件名')

    def __str__(self):
        return self.product_id
    class Meta:
        managed = True
        db_table = 'wms_product'
        db_table_comment = '产品信息表'

# 布料颜色表
class WmsProductColor(models.Model):
    color_id = models.CharField(unique=True, max_length=10, blank=True, null=True, db_comment='颜色编号')
    color_name = models.CharField(max_length=10, blank=True, null=True, db_comment='颜色名称')
    def __str__(self):
        return self.color_name or self.color_id
    class Meta:
        managed = True
        db_table = 'wms_product_color'
        db_table_comment = '布料颜色表'

# 布料品种表
class WmsProductFabricType(models.Model):
    fabric_type_id = models.CharField(unique=True, max_length=10, blank=True, null=True, db_comment='布料品种id')
    fabric_type_name = models.CharField(max_length=10, blank=True, null=True, db_comment='布料品种名称')
    def __str__(self):
        return self.fabric_type_name or self.fabric_type_id
    class Meta:
        managed = True
        db_table = 'wms_product_fabric_type'
        db_table_comment = '布料品种表'

# 库位物料表
class WmsBinStorage(models.Model):
    id = models.CharField(primary_key=True, max_length=50, db_comment='库位id')
    loc_id = models.CharField(unique=True, max_length=50, blank=True, null=True, db_comment='库位编码')
    bin_level = models.IntegerField(blank=True, null=True, db_comment='层')
    bin_row = models.IntegerField(blank=True, null=True, db_comment='排')
    bin_column = models.IntegerField(blank=True, null=True, db_comment='列')
    product = models.ForeignKey('WmsProduct', models.DO_NOTHING, to_field='product_id', blank=True, null=True, db_comment='物料id')
    quantity = models.IntegerField(blank=True, null=True, db_comment='存储数量')
    min_threshold = models.IntegerField(blank=True, null=True, db_comment='最小库存预警阈值')
    def __str__(self):
        return self.loc_id or self.id
    class Meta:
        managed = True
        db_table = 'wms_bin_storage'
        db_table_comment = '库位物料'

# 客户信息表
class WmsCustomer(models.Model):
    customers_id = models.CharField(unique=True, max_length=10, blank=True, null=True, db_comment='企业代号')
    company_name = models.CharField(max_length=20, blank=True, null=True, db_comment='企业名称')
    area = models.IntegerField(blank=True, null=True, db_comment='企业类型1镇内2镇外')
    level = models.IntegerField(blank=True, null=True, db_comment='企业评级')
    principal = models.CharField(max_length=10, blank=True, null=True, db_comment='负责人')
    phone = models.CharField(max_length=10, blank=True, null=True, db_comment='负责人电话')
    email = models.CharField(max_length=50, blank=True, null=True, db_comment='负责人邮箱')
    gender = models.IntegerField(blank=True, null=True, db_comment='联系人性别1男2女')
    create_at = models.DateTimeField(blank=True, null=True, db_comment='加入时间')

    class Meta:
        managed = True
        db_table = 'wms_customer'
        db_table_comment = '客户'


# 库存盘点信息表
class WmsStockCheck(models.Model):
    product = models.ForeignKey('WmsProduct', models.DO_NOTHING, to_field='product_id', blank=True, null=True)
    expected_qty = models.IntegerField()
    actual_qty = models.IntegerField()
    checked_by = models.CharField(max_length=50, blank=True, null=True)
    check_time = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'wms_stock_check'
        db_table_comment = '库存盘点记录表'
