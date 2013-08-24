from django.conf import settings
from django.core.mail import send_mail


def send_email(subject, message, to=None):
    if len(settings.ADMINS) is 0:
        return
    if to is None:
        to = [settings.ADMINS[0][1], ]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)
