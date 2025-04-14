from apscheduler.schedulers.background import BackgroundScheduler
from .models import Book,Lending
from accounts.models import User
from django.db.models import Q
import datetime
from django.utils.timezone import now
from django.core.mail import send_mail
from datetime import timedelta
from django.conf import settings

def send_reminder_emails():
    tomorrow = now().date() + timedelta(days=1)
    tomorrow_str = f"{tomorrow.month}月{tomorrow.day}日"

    lendingslend = Lending.objects.filter(
        Q(date=tomorrow)
    )
    lendingsreturn = Lending.objects.filter(
        is_returned=False,
    ).filter(
        Q(returndate=tomorrow)
    )

    for lending in lendingslend:
        user = lending.username
        subject = "【図書館からの通知】貸出予定のお知らせ"
        message = f"{user.username}様\n\n" \
                  f"明日 {tomorrow_str} に、貸出の予定があります。\n\n" \
                  f"書籍: {lending.book.title}\n" \
                  f"場所: {lending.book.place}\n\n" \
                  f"どうぞよろしくお願いいたします。"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

    for lending in lendingsreturn:
        user = lending.username
        subject = "【図書館からの通知】返却予定のお知らせ"
        message = f"{user.username}様\n\n" \
                  f"明日 {tomorrow_str} に、返却の予定があります。\n\n" \
                  f"書籍: {lending.book.title}\n" \
                  f"場所: {lending.book.place}\n\n" \
                  f"どうぞよろしくお願いいたします。"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

# 毎日０時に貸出日になった本を貸出中にする
def my_job():
    today = datetime.date.today()
    lendings_today = Lending.objects.filter(date=today)

    for item in lendings_today:
        item.book.is_borrowed = True
        item.book.save()

        item.is_returned = False
        item.save()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_job, 'cron', hour=0, minute=1)
    scheduler.add_job(send_reminder_emails, 'cron', hour=0, minute=1)
    scheduler.start()