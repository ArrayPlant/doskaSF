from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import UserRegistrationForm, UserConfirmForm

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # отправляем e-mail
            send_mail(
                subject="Подтверждение регистрации",
                message=f"Здравствуйте!\nВаш код подтверждения: {user.confirmation_code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            messages.success(request, "Вы успешно зарегистрировались! Проверьте почту и введите код.")
            return redirect('accounts:confirm')
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def confirm_registration(request):
    if request.method == "POST":
        form = UserConfirmForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            code = form.cleaned_data["code"]
            try:
                user = User.objects.get(email=email, confirmation_code=code)
                user.is_confirmed = True
                user.save()
                login(request, user)  # автоматически логиним
                messages.success(request, "Ваш аккаунт подтверждён!")
                return redirect('board:my_ads')  # сразу переходим в ЛК
            except User.DoesNotExist:
                messages.error(request, "Неверный email или код подтверждения.")
    else:
        form = UserConfirmForm()
    return render(request, "accounts/confirm.html", {"form": form})
