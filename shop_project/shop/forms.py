from django import forms
from .models import ReturnRequest, OrderItem

class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ['order_item', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'order_item': forms.Select(attrs={'class': 'form-select'}),
        }
