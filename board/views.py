from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import Announcement, Response
from .forms import AnnouncementForm, ResponseForm

@login_required
def create_announcement(request):
    if not request.user.is_confirmed:
        messages.error(request, "Вы должны подтвердить свою регистрацию, прежде чем создавать объявления.")
        return redirect("board:my_ads")

    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.author = request.user
            ann.save()
            messages.success(request, "Объявление успешно создано!")
            return redirect("board:my_ads")
    else:
        form = AnnouncementForm()
    return render(request, "board/create_ad.html", {"form": form})


@login_required
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, author=request.user)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Объявление обновлено!")
            return redirect("board:my_ads")
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, "board/edit_ad.html", {"form": form, "announcement": announcement})


@login_required
def my_advertisements(request):
    ads = Announcement.objects.filter(author=request.user)
    return render(request, "board/my_ads.html", {"ads": ads})


@login_required
def detail_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.announcement = announcement
            response.user = request.user
            response.save()
            # Уведомляем автора объявления по e-mail
            send_mail(
                subject="Новый отклик на ваше объявление",
                message=(
                    f"На ваше объявление '{announcement.title}' поступил новый отклик.\n\n"
                    f"Текст отклика: {response.text}\n\n"
                    f"От пользователя: {request.user.username}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[announcement.author.email],
            )
            messages.success(request, "Отклик отправлен!")
            return redirect("board:detail_ad", pk=announcement.pk)
    else:
        form = ResponseForm()

    return render(request, "board/detail_ad.html", {"announcement": announcement, "form": form})


@login_required
def responses_dashboard(request):
    user_announcements = Announcement.objects.filter(author=request.user)
    announcement_id = request.GET.get("announcement")
    if announcement_id:
        responses = Response.objects.filter(announcement__in=user_announcements, announcement_id=announcement_id)
    else:
        responses = Response.objects.filter(announcement__in=user_announcements)

    return render(request, "board/responses_dashboard.html", {
        "responses": responses,
        "user_announcements": user_announcements,
        "selected_announcement": announcement_id,
    })


@login_required
def delete_response(request, pk):
    response = get_object_or_404(Response, pk=pk, announcement__author=request.user)
    response.delete()
    messages.success(request, "Отклик удалён.")
    return redirect("board:responses_dashboard")


@login_required
def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk, announcement__author=request.user)
    response.is_accepted = True
    response.save()
    # Уведомление автора отклика
    send_mail(
        subject="Ваш отклик принят!",
        message=(
            f"Поздравляем! Ваш отклик на объявление '{response.announcement.title}' был принят.\n\n"
            "Свяжитесь с автором для дальнейших подробностей."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.user.email],
    )
    messages.success(request, "Отклик принят.")
    return redirect("board:responses_dashboard")
