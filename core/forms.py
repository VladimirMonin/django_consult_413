from django import forms
from .models import Order, Service, Review
from django.utils import timezone
from datetime import datetime


class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["name", "text", "rating", "master", "photo"]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "rating": forms.Select(attrs={"class": "form-control"}),
            "master": forms.Select(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
        }


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
        fields = ["name", "phone", "comment", "master", "appointment_date", "services"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Ваше имя", "class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "+7 (999) 999-99-99", "class": "form-control"}
            ),
            "comment": forms.Textarea(
                attrs={
                    "placeholder": "Комментарий к заказу",
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "master": forms.Select(attrs={"class": "form-select"}),
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

    def clean_services(self):
        # Нам нужно добыть мастера и все указанные услуги из формы, добыть их из DB и проверить действительно ли мастер
        # Предоставляет все эти услуги

        services = self.cleaned_data.get("services")
        master = self.cleaned_data.get("master")

        if not master or not services:
            raise forms.ValidationError("Вы должны выбрать мастера и услуги.")

        # Добывам все услуги которые предоставяет этот мастер на смом деле
        master_services = master.services.all()

        # Проверяем все ли услуги которые выбрал пользователь предоставляет этот мастер
        not_approved_services = []
        for service in services:
            if service not in master_services:
                not_approved_services.append(service.name)

        if not_approved_services:
            raise forms.ValidationError("Этот мастер не предоставляет следующие услуги: " + ", ".join(not_approved_services))
        
        
        return services
