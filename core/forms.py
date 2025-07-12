from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'services', 'appointment_date']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99', 'class': 'form-control'}),
            'services': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }