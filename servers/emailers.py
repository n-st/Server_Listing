from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string


def send_email(subject, message, to=None):
    if len(settings.ADMINS) is 0:
        return
    if to is None:
        to = [settings.ADMINS[0][1], ]

    msg = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=to)
    msg.content_subtype = "html"
    msg.send()


def send_failure(ping_object, server_log):
    email = render_to_string('servers/emails/email_failure.html', {
        "ping": ping_object,
        "server_log": server_log,
        "server": server_log.server,
    })
    send_email(
        subject="Server {} went down!".format(server_log.server.name),
        message=email,
    )


def send_back_up(ping_object, server_log):
    email = render_to_string('servers/emails/email_up.html', {
        "ping": ping_object,
        "server_log": server_log,
        "server": server_log.server,
    })
    send_email(
        subject="Server {} is back up!".format(server_log.server.name),
        message=email,
    )
