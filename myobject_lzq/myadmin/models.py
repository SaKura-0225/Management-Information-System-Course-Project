'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2025-04-22 16:31:29
LastEditors: SaKura0225 2948196205@qq.com
LastEditTime: 2025-06-12 20:05:46
FilePath: \code\myobject_lzq\myadmin\models.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.db import models
from datetime import datetime


# Create your models here.
class User1(models.Model):

    username = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    password_hash = models.CharField(max_length=100, blank=True, null=True)
    password_salt = models.CharField(max_length=50, blank=True, null=True)
    status = models.PositiveIntegerField()
    create_at = models.DateTimeField(blank=True, null=True)
    update_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'user1'
class User(models.Model):
    username = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=100)
    password_salt = models.CharField(max_length=50)
    status = models.IntegerField(default=1)   # 状态：1正常 2禁用3管理员 9删除
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)


    def toDict(self):
        return {'id': self.id, 'username': self.username, 'nickname': self.nickname,
                'password_hash': self.password_hash}

    class Meta:
        db_table = "user"


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
        db_table = "shop"  # 更改表名

# 菜品类别数据
class Category(models.Model):
    shop_id = models.IntegerField()        # 店铺id
    name = models.CharField(max_length=50) # 分类名称
    status = models.IntegerField(default=1)        # 状态:1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)    # 创建时间
    update_at = models.DateTimeField(default=datetime.now)    # 修改时间

    class Meta:
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
        db_table = "product"  # 更改表名

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

# 订单信息表
class Orders(models.Model):
    shop_id = models.PositiveIntegerField(blank=True, null=True, db_comment='店铺id号')
    member_id = models.PositiveIntegerField(blank=True, null=True, db_comment='会员id')
    user_id = models.PositiveIntegerField(blank=True, null=True, db_comment='操作员id')
    money = models.FloatField(blank=True, null=True, db_comment='金额')
    status = models.PositiveIntegerField(blank=True, null=True, db_comment='订单状态:1过行中/2无效/3已完成')
    payment_status = models.PositiveIntegerField(blank=True, null=True, db_comment='支付状态:1未支付/2已支付/3已退款')
    create_at = models.DateTimeField(blank=True, null=True, db_comment='添加时间')
    update_at = models.DateTimeField(blank=True, null=True, db_comment='修改时间')

    class Meta:
        managed = False
        db_table = 'orders'

# 订单信息表具体版
class Order2(models.Model):
    shopname = models.CharField(max_length=255, db_collation='utf8mb3_general_ci', db_comment='店铺名称')
    membername = models.CharField(max_length=50, db_collation='utf8mb3_general_ci', blank=True, null=True, db_comment='昵称')
    usernickname = models.CharField(max_length=50, db_collation='utf8mb3_general_ci', blank=True, null=True, db_comment='昵称')
    money = models.FloatField(blank=True, null=True, db_comment='金额')
    status = models.PositiveIntegerField(blank=True, null=True, db_comment='订单状态:1过行中/2无效/3已完成')
    create_at = models.DateTimeField(blank=True, null=True, db_comment='添加时间')
    update_at = models.DateTimeField(blank=True, null=True, db_comment='修改时间')

    class Meta:
        managed = False
        db_table = 'order2'


#布料销售订单
class WmsOrders(models.Model):
    user_id = models.IntegerField(blank=True, null=True, db_comment='操作员id')
    create_at = models.DateTimeField(blank=True, null=True, db_comment='下单时间')
    orders_id = models.IntegerField(primary_key=True, db_comment='订单编号')
    total_amount = models.IntegerField(blank=True, null=True, db_comment='面料出库总量')
    category = models.IntegerField(blank=True, null=True, db_comment='1：镇内订单  2：镇外订单')
    payment_status = models.IntegerField(blank=True, null=True, db_comment='支付状态:1未支付/2已支付/3已退款')
    update_at = models.CharField(max_length=30, blank=True, null=True, db_comment='更新时间')

    class Meta:
        managed = False
        db_table = 'wms_orders'
        db_table_comment = '销售订单表'

#布料销售订单详情
class WmsOrdersDetail(models.Model):
    price = models.FloatField(db_comment='单价')
    total_price = models.FloatField()
    orders_id = models.IntegerField(primary_key=True, db_comment='订单编号')
    product_id = models.CharField(max_length=45)
    quantity = models.IntegerField()
    status = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'wms_orders_detail'