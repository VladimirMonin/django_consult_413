from django import forms
from .models import Order


class ServiceForm(forms.Form):
    # class': 'form-control
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Название услуги"}
        ),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Описание услуги", "class": "form-control"}
        ),
        help_text="Введите продающее описание услуги",
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    duration = forms.IntegerField(
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    is_popular = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    image = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"}), help_text="Квадратное изображение не меньше 500х500"
    )


# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['name', 'phone', 'services', 'appointment_date']
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-control'}),
#             'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99', 'class': 'form-control'}),
#             'services': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
#             'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#         }
