# views/product.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from myadmin.models import WmsProduct, WmsProductColor, WmsProductFabricType, WmsBinStorage
from .forms import ProductForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('myadmin.view_wmsproduct', raise_exception=True)
def index(request):
    query = WmsProduct.objects.select_related('fabric_type', 'color', 'loc')

    # 获取搜索参数
    keyword = request.GET.get('keyword', '').strip()
    fabric_type_id = request.GET.get('fabric_type')
    color_id = request.GET.get('color')

    # 组合过滤条件
    if keyword:
        query = query.filter(product_id__icontains=keyword)

    if fabric_type_id:
        query = query.filter(fabric_type__id=fabric_type_id)

    if color_id:
        query = query.filter(color__id=color_id)

    # 分页
    paginator = Paginator(query.order_by('id'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 渲染模板
    return render(request, 'myadmin/product/index.html', {
        'page_obj': page_obj,
        'fabric_types': WmsProductFabricType.objects.all(),
        'colors': WmsProductColor.objects.all(),
    })

@login_required
@permission_required('myadmin.view_wmsproduct', raise_exception=True)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myadmin_product_index')
    else:
        form = ProductForm()
    return render(request, 'myadmin/product/add.html', {'form': form})

@login_required
@permission_required('myadmin.view_wmsproduct', raise_exception=True)
def edit_product(request, id):
    product = get_object_or_404(WmsProduct, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('myadmin_product_index')
    else:
        form = ProductForm(instance=product)
    return render(request, 'myadmin/product/edit.html', {'form': form})

@login_required
@permission_required('myadmin.view_wmsproduct', raise_exception=True)
def product_delete(request, id):
    product = get_object_or_404(WmsProduct, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('myadmin_product_index')
    return render(request, 'myadmin/product/delete.html', {'product': product})
