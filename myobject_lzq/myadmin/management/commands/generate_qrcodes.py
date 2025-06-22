from django.core.management.base import BaseCommand
from django.conf import settings
from myadmin.models import WmsProduct
import os
import qrcode

class Command(BaseCommand):
    help = '为所有产品生成二维码并保存到 static/qrcodes/product 下，同时更新 barcode_file 字段'

    def handle(self, *args, **options):
        folder = os.path.join(settings.BASE_DIR, 'static', 'qrcodes', 'product')
        os.makedirs(folder, exist_ok=True)

        products = WmsProduct.objects.select_related('fabric_type', 'color', 'loc').filter(
            product_id__isnull=False,
            fabric_type__isnull=False,
            color__isnull=False,
            loc__isnull=False,
        )

        for product in products:
            try:
                # 内容支持中文
                content = f"SKU: {product.product_id}\n品种: {product.fabric_type.fabric_type_name}\n颜色: {product.color.color_name}\n库位: {product.loc.loc_id}"
                filename = f"{product.product_id}.png"
                path = os.path.join(folder, filename)

                # 生成二维码并保存
                img = qrcode.make(content)
                img.save(path)

                # 更新数据库字段
                product.barcode_file = filename
                product.save()

                self.stdout.write(self.style.SUCCESS(f"[√] 已生成二维码: {filename}"))
            except Exception as e:
                self.stderr.write(f"[×] {product.product_id} 生成失败: {e}")
