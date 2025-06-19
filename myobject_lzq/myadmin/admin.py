
from django.contrib import admin
<<<<<<< HEAD
from .models import WmsOrders
# Register your models here.

=======
from .models import Product, WmsOrders
# Register your models here.

admin.site.register(Product)
>>>>>>> dd7dd62 (系统管理功能1)
admin.site.register(WmsOrders)