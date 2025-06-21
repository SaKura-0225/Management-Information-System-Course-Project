
from django import forms
from myadmin.models import WmsOrders,WmsOutbound,WmsOrdersDetail
from django.contrib.auth.models import User, Group
from myadmin.models import EmployeeProfile, Department, WmsCustomer, WmsProduct, WmsStockCheck

class AddOrdersInfoForm(forms.ModelForm):
    class Meta:
        model = WmsOrders
        fields = '__all__'
        widgets = {
            'create_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'update_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(choices=[
                (1, '镇内订单'),
                (2, '镇外订单')
            ]),
            'payment_status': forms.Select(choices=[
                (1, '未支付'),
                (2, '已支付'),
                (3, '已退款')
            ]),
            'status': forms.Select(choices=[
                (1, '已拣货'),
                (2, '未拣货')
            ]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 增加统一的样式支持（如使用 Bootstrap）
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

class AddWarehouseInfoForm(forms.ModelForm):
    class Meta:
        model = WmsOutbound
        fields = '__all__'
        widgets = {
            'create_at': forms.DateInput(attrs={'type': 'date'}),
            'update_at': forms.DateInput(attrs={'type': 'date'}),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'groups']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['department', 'work_no', 'phone']


class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = WmsOrdersDetail
        exclude = ['orders']  # orders 在视图中动态设置
        widgets = {
            'product_id': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = WmsCustomer
        fields = ['customers_id', 'company_name', 'area', 'level', 'principal', 'phone', 'email', 'gender', 'create_at']
        widgets = {
            'create_at': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_customers_id(self):
        cid = self.cleaned_data.get('customers_id')
        if not cid:
            raise forms.ValidationError("客户代号不能为空")
        return cid


class ProductForm(forms.ModelForm):
    class Meta:
        model = WmsProduct
        fields = ['product_id', 'fabric_type', 'color', 'loc', 'price']
        widgets = {
            'product_id': forms.TextInput(attrs={'class': 'form-control'}),
            'fabric_type': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'loc': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StockCheckForm(forms.ModelForm):
    class Meta:
        model = WmsStockCheck
        fields = ['actual_qty', 'checked_by', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }