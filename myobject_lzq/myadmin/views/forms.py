
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


class EmployeeForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    email = forms.EmailField(required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
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
