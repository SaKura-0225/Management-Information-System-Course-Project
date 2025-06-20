
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
<<<<<<< HEAD
<<<<<<< HEAD
=======


# 店铺信息
class Shop(models.Model):
    name = models.CharField(max_length=255)        # 店铺名称
    cover_pic = models.CharField(max_length=255)   # 封面图片
    banner_pic = models.CharField(max_length=255)  # 图标Logo
    address = models.CharField(max_length=255)     # 店铺地址
    phone = models.CharField(max_length=255)       # 联系电话
    status = models.IntegerField(default=1)        # 状态:1正常/2暂停/9删除
    create_at = models.DateTimeField(default=datetime.now)    # 创建时间
    update_at = models.DateTimeField(default=datetime.now)    # 修改时间

    def toDict(self):
        shopname = self.name.split("-")
        return {'id': self.id, 'name': shopname[0], 'shop': shopname[1], 'cover_pic': self.cover_pic, 'banner_pic': self.banner_pic, 'address': self.address, 'phone': self.phone, 'status': self.status, 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'), 'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        managed = False
        db_table = "shop"  # 更改表名

# 菜品类别数据
class Category(models.Model):
    shop_id = models.IntegerField()        # 店铺id
    name = models.CharField(max_length=50) # 分类名称
    status = models.IntegerField(default=1)        # 状态:1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)    # 创建时间
    update_at = models.DateTimeField(default=datetime.now)    # 修改时间

    class Meta:
        managed = False
        db_table = "category"  # 更改表名

#菜品信息模型
class Product(models.Model):
    shop_id = models.IntegerField()        #店铺id
    category_id = models.IntegerField()    #菜品分类id
    cover_pic = models.CharField(max_length=50)    #菜品图片
    name = models.CharField(max_length=50)#菜品名称
    price = models.FloatField()    #菜品单价
    status = models.IntegerField(default=1)        #状态:1正常/2停售/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        return {'id':self.id,'shop_id':self.shop_id,'category_id':self.category_id,'cover_pic':self.cover_pic,'name':self.name,'price':self.price,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        managed = False
        db_table = "product"  # 更改表名

>>>>>>> f7fabbd (消除原始代码影响1)
=======
>>>>>>> 1999e5d (消除原始代码影响2)
# 会员信息表
class Member(models.Model):
    nickname = models.CharField(max_length=50)    #昵称
    avatar = models.CharField(max_length=255)    #头像
    mobile = models.CharField(max_length=50)    #电话
    status = models.IntegerField(default=1)        #状态:1正常/2禁用/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        return {'id':self.id,'nickname':self.nickname,'avatar':self.avatar,'mobile':self.mobile,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "member"  # 更改表名

#布料销售订单
class WmsOrders(models.Model):
    orders_id = models.IntegerField(primary_key=True, db_comment='订单编号')
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
=======
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True, db_comment='操作员id')
>>>>>>> 92d8e23 (1)
=======
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
>>>>>>> 9851b42 (基本完成订单管理，出库管理和系统管理)
=======
>>>>>>> 6c0dbd3 (添加模型)
    total_amount = models.IntegerField(blank=True, null=True, db_comment='面料出库总量')
    category = models.IntegerField(blank=True, null=True, db_comment='1：镇内订单  2：镇外订单')
    payment_status = models.IntegerField(blank=True, null=True, db_comment='财务状态:1未到账/2已到账')
    customer = models.ForeignKey('WmsCustomer', models.DO_NOTHING, to_field='customers_id', blank=True, null=True, db_comment='采购企业代号')
    work_no = models.ForeignKey('MyadminEmployeeprofile', models.DO_NOTHING, db_column='work_no', to_field='work_no', blank=True, null=True, db_comment='拣货员工号')
    status = models.IntegerField(blank=True, null=True, db_comment='1:已拣货  2:未拣货')
    qrcode = models.CharField(max_length=100, blank=True, null=True, db_comment='拣货单二维码')
    create_at = models.DateTimeField(blank=True, null=True, db_comment='下单时间')
    update_at = models.DateTimeField(blank=True, null=True, db_comment='更新时间')

    class Meta:
        managed = False
        db_table = 'wms_orders'
        db_table_comment = '销售订单表'
<<<<<<< HEAD
      
<<<<<<< HEAD
#布料销售订单详情
<<<<<<< HEAD
class WmsOrdersDetail(models.Model):
    orders = models.ForeignKey('WmsOrders', models.DO_NOTHING, db_comment='订单编号')
    product_id = models.CharField(max_length=45)
    quantity = models.IntegerField()
    price = models.FloatField(db_comment='单价')
    total_price = models.FloatField()
    status = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'wms_orders_detail'
=======
=======
#布料销售订单详情1
>>>>>>> 92d8e23 (1)
class OrdersDetailWithDates(models.Model):
    orders_id = models.IntegerField(db_comment='订单编号')
    product_id = models.CharField(max_length=45, db_collation='utf8mb4_0900_ai_ci')
    quantity = models.IntegerField()
    price = models.FloatField(db_comment='单价')
    total_price = models.FloatField()
    status = models.CharField(max_length=45, db_collation='utf8mb4_0900_ai_ci')
    create_at = models.DateTimeField(blank=True, null=True, db_comment='下单时间')
    update_at = models.DateTimeField(blank=True, null=True, db_comment='更新时间')

    class Meta:
        managed = False
        db_table = 'orders_detail_with_dates'
>>>>>>> f7fabbd (消除原始代码影响1)
=======
>>>>>>> 9851b42 (基本完成订单管理，出库管理和系统管理)

#布料销售订单详情
class WmsOrdersDetail(models.Model):
    orders = models.ForeignKey('WmsOrders', models.DO_NOTHING, db_comment='订单编号')
    product = models.ForeignKey('WmsProduct', models.DO_NOTHING, to_field='product_id', blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True, db_comment='单价')
    total_price = models.FloatField(blank=True, null=True)
    create_at = models.DateTimeField(blank=True, null=True, db_comment='下单日期')

    class Meta:
        managed = False
        db_table = 'wms_orders_detail'

#出库表
class WmsOutbound(models.Model):
    orders_id = models.IntegerField(blank=True, null=True, db_comment='采购订单id')
    name = models.CharField(max_length=50, blank=True, null=True, db_comment='物料名称')
    product_id = models.IntegerField(blank=True, null=True, db_comment='SKU编号')
    quantity = models.IntegerField(blank=True, null=True, db_comment='数量')
    bin_id = models.IntegerField(blank=True, null=True, db_comment='库位编号')
    user_id = models.IntegerField(blank=True, null=True, db_comment='操作员id')
    create_at = models.DateTimeField(blank=True, null=True, db_comment='出库时间')
    update_at = models.DateTimeField(blank=True, null=True, db_comment='更新时间')

    class Meta:
        managed = False
        db_table = 'wms_outbound'


# 部门表
class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class MyadminDepartment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    code = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
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
    
class MyadminEmployeeprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    work_no = models.CharField(unique=True, max_length=100)
    gender = models.IntegerField(blank=True, null=True, db_comment='性别 男1/女2')
    phone = models.CharField(max_length=20)
    department = models.ForeignKey('MyadminDepartment', models.DO_NOTHING, blank=True, null=True)
    user_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'myadmin_employeeprofile'
    
# 产品信息表
class WmsProduct(models.Model):
    product_id = models.CharField(unique=True, max_length=10, blank=True, null=True, db_comment='产品编号')
    fabric_type = models.ForeignKey('WmsProductFabricType', models.DO_NOTHING, to_field='fabric_type_id', blank=True, null=True, db_comment='布料品种id')
    color = models.ForeignKey('WmsProductColor', models.DO_NOTHING, to_field='color_id', blank=True, null=True, db_comment='布料颜色id')
    loc = models.ForeignKey('WmsBinStorage', models.DO_NOTHING, to_field='loc_id', blank=True, null=True, db_comment='库位编码')
    price = models.IntegerField(blank=True, null=True, db_comment='单价')

    class Meta:
        managed = False
        db_table = 'wms_product'
        db_table_comment = '产品信息表'

# 布料颜色表
class WmsProductColor(models.Model):
    color_id = models.CharField(unique=True, max_length=10, blank=True, null=True, db_comment='颜色编号')
    color_name = models.CharField(max_length=10, blank=True, null=True, db_comment='颜色名称')

    class Meta:
        managed = False
        db_table = 'wms_product_color'
        db_table_comment = '布料颜色表'

# 布料品种表
class WmsProductFabricType(models.Model):
    fabric_type_id = models.CharField(unique=True, max_length=10, blank=True, null=True, db_comment='布料品种id')
    fabric_type_name = models.CharField(max_length=10, blank=True, null=True, db_comment='布料品种名称')

    class Meta:
        managed = False
        db_table = 'wms_product_fabric_type'
        db_table_comment = '布料品种表'

# 库位物料表
class WmsBinStorage(models.Model):
    id = models.CharField(primary_key=True, max_length=50, db_comment='库位id')
    loc_id = models.CharField(unique=True, max_length=50, blank=True, null=True, db_comment='库位编码')
    bin_level = models.IntegerField(blank=True, null=True, db_comment='层')
    bin_row = models.IntegerField(blank=True, null=True, db_comment='排')
    bin_column = models.IntegerField(blank=True, null=True, db_comment='列')
    product_id = models.CharField(max_length=50, blank=True, null=True, db_comment='物料id')
    quantity = models.IntegerField(blank=True, null=True, db_comment='存储数量')

    class Meta:
        managed = False
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
        managed = False
        db_table = 'wms_customer'
        db_table_comment = '客户'