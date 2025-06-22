from django.shortcuts import render, get_object_or_404, redirect
from myadmin.models import WmsCustomer
from myadmin.views.forms import CustomerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required('myadmin.view_wmscustomer', raise_exception=True)
def index(request):
    customer_list = WmsCustomer.objects.order_by('-create_at')  # 按加入时间倒序排列
    paginator = Paginator(customer_list, 10)  # 每页 10 条

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'myadmin/customer/index.html', {
        'page_obj': page_obj,
    })

@login_required
@permission_required('myadmin.view_wmscustomer', raise_exception=True)
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myadmin_customer_index')
    else:
        form = CustomerForm()
    return render(request, 'myadmin/customer/add.html', {'form': form})

@login_required
@permission_required('myadmin.view_wmscustomer', raise_exception=True)
def edit_customer(request, id):
    customer = get_object_or_404(WmsCustomer, pk=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('myadmin_customer_index')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'myadmin/customer/edit.html', {'form': form, 'customer': customer})

@login_required
@permission_required('myadmin.view_wmscustomer', raise_exception=True)
def customer_delete(request, id):
    customer = get_object_or_404(WmsCustomer, pk=id)
    if request.method == 'POST':
        customer.delete()
        return redirect('myadmin_customer_index')
    return render(request, 'myadmin/customer/delete.html', {'customer': customer})
