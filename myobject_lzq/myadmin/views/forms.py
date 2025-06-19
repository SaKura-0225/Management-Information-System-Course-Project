
from django import forms
<<<<<<< HEAD
<<<<<<< HEAD
from myadmin.models import WmsOrders,WmsOutbound,WmsOrdersDetail
=======
from myadmin.models import WmsOrders,WmsOutbound
>>>>>>> dd7dd62 (系统管理功能1)
=======
from myadmin.models import WmsOrders,WmsOutbound,WmsOrdersDetail
>>>>>>> 9851b42 (基本完成订单管理，出库管理和系统管理)
from django.contrib.auth.models import User, Group
from myadmin.models import EmployeeProfile, Department

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


<<<<<<< HEAD
<<<<<<< HEAD
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
=======
class EmployeeForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    email = forms.EmailField(required=False)
>>>>>>> dd7dd62 (系统管理功能1)
=======
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
>>>>>>> 1999e5d (消除原始代码影响2)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 1999e5d (消除原始代码影响2)
        model = User
        fields = ['username', 'email', 'password', 'groups']


class EmployeeForm(forms.ModelForm):
    class Meta:
<<<<<<< HEAD
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
<<<<<<< HEAD
=======
        model = EmployeeProfile
        fields = ['department', 'work_no', 'phone', 'post']

    def save(self, commit=True):
        employee = super().save(commit=False)

        if not hasattr(employee, 'user'):
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password']
            )
            user.email = self.cleaned_data['email']
            employee.user = user
        else:
            user = employee.user
            user.email = self.cleaned_data['email']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])

        if commit:
            employee.save()
            user.save()
            user.groups.set(self.cleaned_data['groups'])

        return employee
>>>>>>> dd7dd62 (系统管理功能1)
=======
        model = EmployeeProfile
        fields = ['department', 'work_no', 'phone']
>>>>>>> 1999e5d (消除原始代码影响2)
=======
>>>>>>> 9851b42 (基本完成订单管理，出库管理和系统管理)
