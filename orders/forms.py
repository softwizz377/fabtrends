from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['username','first_name', 'last_name', 'email','phone_number','house_number','town','city','district','state','country','postal_code','full_address']
        
class RequestRefundForm(forms.Form):
    order_id = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()