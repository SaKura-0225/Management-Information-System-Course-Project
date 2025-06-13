from django import forms
from myadmin.models import WmsOrders

class AddOrdersInfoForm(forms.ModelForm):
    class Meta:
        model = WmsOrders
        fields = '__all__'
        widgets = {
            'create_at': forms.DateInput(attrs={'type': 'date'}),
            'update_at': forms.DateInput(attrs={'type': 'date'}),
        }