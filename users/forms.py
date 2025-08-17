# users/forms.py
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
    SetPasswordForm,
    PasswordResetForm,
)
from django import forms

# get_user_model - получает модель пользователя автоматически, и нам не страшно если мы поменяем модель пользователя в будущем
from django.contrib.auth import get_user_model

# Мы поменяли модель пользователя, но так как используется get_user_model нам не надо ничего менять!)
user_model = get_user_model()


class CustomSetPasswordForm(SetPasswordForm):
    """
    Форма установки нового пароля (шаг 5)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class CustomPasswordResetForm(PasswordResetForm):
    """
    Форма ввода емейла для сброса пароля (шаг 2)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Форма смены пароля (например в личном кабинете) - когда знаем старый пароль
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = user_model
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Циклом определяем всем полям form-control
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if user_model.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
