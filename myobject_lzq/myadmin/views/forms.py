
from django import forms
from myadmin.models import WmsOrders,WmsOutbound
from django.contrib.auth.models import User, Group
from myadmin.models import EmployeeProfile, Department

class AddOrdersInfoForm(forms.ModelForm):
    class Meta:
        model = WmsOrders
        fields = '__all__'
        widgets = {
            'create_at': forms.DateInput(attrs={'type': 'date'}),
            'update_at': forms.DateInput(attrs={'type': 'date'}),
        }

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
