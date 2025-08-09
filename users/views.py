from django.shortcuts import render
from .forms import CustomRegisterForm, CustomLoginForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy


class CustomRegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name = "users_login_registr.html"
    success_url = "/users/login/"
    success_message = "Вы успешно зарегистрировались! Добро пожаловать!"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        # Сразу авторизуем пользователя после регистрации
        login(self.request, form.instance)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Ошибка регистрации. Пожалуйста, проверьте введенные данные."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Регистрация"
        return context


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("landing")
    success_message = "Вы успешно вошли в систему!"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Ошибка входа. Пожалуйста, проверьте введенные данные."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Вход"
        return context


class CustomLogoutView(LogoutView):
    next_page = "/"
