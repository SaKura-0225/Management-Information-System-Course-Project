# views/product.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from myadmin.models import WmsProduct, WmsProductColor, WmsProductFabricType, WmsBinStorage
from .forms import ProductForm

def index(request):
    query = WmsProduct.objects.select_related('fabric_type', 'color', 'loc')
    paginator = Paginator(query.order_by('id'), 10)  # 每页10条
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myadmin/product/index.html', {'page_obj': page_obj})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myadmin_product_index')
    else:
        form = ProductForm()
    return render(request, 'myadmin/product/add.html', {'form': form})

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

def product_delete(request, id):
    product = get_object_or_404(WmsProduct, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('myadmin_product_index')
    return render(request, 'myadmin/product/delete.html', {'product': product})
