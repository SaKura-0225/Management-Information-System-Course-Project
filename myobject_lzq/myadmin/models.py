
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
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    total_amount = models.IntegerField(blank=True, null=True, db_comment='面料出库总量')
    category = models.IntegerField(blank=True, null=True, db_comment='1：镇内订单  2：镇外订单')
    payment_status = models.IntegerField(blank=True, null=True, db_comment='支付状态:1未支付/2已支付/3已退款')
    status = models.IntegerField(blank=True, null=True, db_comment='1:已拣货  2:未拣货')
    create_at = models.DateTimeField(blank=True, null=True, db_comment='下单时间')
    update_at = models.DateTimeField(blank=True, null=True, db_comment='更新时间')

    class Meta:
        managed = False
        db_table = 'wms_orders'
        db_table_comment = '销售订单表'
      
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

# 员工扩展信息（绑定用户）

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_constraint=False)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    work_no = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    post = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username