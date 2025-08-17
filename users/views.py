from django.shortcuts import redirect
from .forms import (
    CustomRegisterForm,
    CustomLoginForm,
    CustomPasswordChangeForm,
    CustomSetPasswordForm,
    CustomPasswordResetForm,
)
from django.views.generic.edit import CreateView
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy


class CustomPasswordResetView(PasswordResetView):
    """
    1. Начало сброса пароля. Человек вводит емейл для сброса
    """

    template_name = "users_login_registr.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("password_reset_done")
    email_template_name = "password_reset_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Восстановление пароля"
        return context


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    2. Загляните в Emeil - вам ушло письмо с инструкциями
    """

    message = "Инструкции по восстановлению пароля отправлены на Email"
    operation_type = "Внимание!"

    template_name = "users_message.html"
    extra_context = {
        "operation_type": operation_type,
        "message": message,
    }


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    3. Вью где отображается форма восстановление пароля (можно попасть только через платформу 9 3\4
    ) - комбо <uidb64> + <token>
    """

    operation_type = "Сменить пароль"
    extra_context = {"operation_type": operation_type}
    form_class = CustomSetPasswordForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Ура! Вы сбросили пароль!
    """
    message = "Вы успешно сменили пароль!"
    operation_type = "Внимание!"
    extra_context = {
        "operation_type": operation_type,
        "message": message,
    }
    template_name = "users_message.html"


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("landing")

    def form_valid(self, form):
        messages.success(self.request, "Пароль успешно изменен!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Смена пароля"
        return context


class CustomRegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("landing")
    success_message = "Вы успешно зарегистрировались! Добро пожаловать!"

    def form_valid(self, form):
        # 1. Сохраняем пользователя. Теперь у объекта user есть ID.
        user = form.save()

        # 2. Устанавливаем self.object, как того требует CreateView.
        self.object = user

        # 3. Теперь безопасно вызываем login().
        login(self.request, user)

        messages.success(self.request, self.success_message)

        # 4. Выполняем перенаправление.
        return redirect(self.get_success_url())

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
    success_url = reverse_lazy("services-list")
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
