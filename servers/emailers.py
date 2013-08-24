from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email(subject, message, to=None):
    if len(settings.ADMINS) is 0:
        return
    if to is None:
        to = [settings.ADMINS[0][1], ]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)


def send_failure(ping_object):
    email = render_to_string('servers/emails/email_failure.html', {
        "ping": ping_object
    })
    send_email(
        subject="Server went down!",
        message=email,
    )