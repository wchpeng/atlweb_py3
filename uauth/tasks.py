from celery import shared_task
from django.core.mail import send_mail

from atlweb_py3.settings import EMAIL_HOST_USER


# 发邮件
@shared_task
def send_email(to_email, subject=None, message=None, html_message=None):
    send_mail(subject=subject,
              from_email=EMAIL_HOST_USER,
              message=message,
              html_message=html_message,
              recipient_list=[to_email]
    )