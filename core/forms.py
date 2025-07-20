from django import forms
from .models import Order, Service
from django.utils import timezone
from datetime import datetime


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Название услуги"}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Описание услуги", "class": "form-control"}
            ),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "duration": forms.NumberInput(attrs={"class": "form-control"}),
            "is_popular": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "description": "Введите продающее описание услуги",
            "image": "Квадратное изображение не меньше 500х500",
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "comment", "appointment_date", "services"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Ваше имя", "class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "+7 (999) 999-99-99", "class": "form-control"}
            ),
            "comment": forms.Textarea(
                attrs={"placeholder": "Комментарий к заказу", "class": "form-control", "rows": 3}
            ),
            "services": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check-input"}
            ),
            "appointment_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get("appointment_date")
        if appointment_date and appointment_date < timezone.now().date():
            raise forms.ValidationError("Дата записи не может быть в прошлом.")
        return appointment_date

