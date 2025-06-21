from django.shortcuts import render
from myadmin.models import WmsBinStorage
from collections import defaultdict

def bin_visualization(request):
    bins = (
        WmsBinStorage.objects
        .select_related('product__fabric_type', 'product__color')
        .all()
    )

    grouped = defaultdict(list)
    for b in bins:
        if not b.product:
            continue
        grouped[b.bin_level or 0].append({
            "bin_row": b.bin_row,
            "bin_column": b.bin_column,
            "quantity": b.quantity or 0,
            "min_threshold": b.min_threshold or 0,
            "product_id": b.product.product_id,
            "fabric_type": b.product.fabric_type.fabric_type_name if b.product.fabric_type else "",
            "color": b.product.color.color_name if b.product.color else "",
            "status": "low" if (b.quantity or 0) < (b.min_threshold or 0) else "normal"
        })

    return render(request, "myadmin/warehouse/index.html", {
        "grouped_bins": dict(grouped)
    })
