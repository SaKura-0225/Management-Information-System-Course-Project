
from django.contrib import admin
<<<<<<< HEAD
<<<<<<< HEAD
from .models import WmsOrders
# Register your models here.

=======
from .models import Product, WmsOrders
# Register your models here.

admin.site.register(Product)
>>>>>>> dd7dd62 (系统管理功能1)
=======
from .models import WmsOrders
# Register your models here.

>>>>>>> 1999e5d (消除原始代码影响2)
admin.site.register(WmsOrders)