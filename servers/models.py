from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from datetime import timedelta


class Server(models.Model):

    MONTHLY = 'm'
    YEARLY = 'y'

    BILLING_CHOICES = (
        (MONTHLY, 'Monthly'),
        (YEARLY, 'Yearly'),
    )

    name = models.CharField(max_length=255)
    notes = models.TextField(default='', blank=True)

    cost = models.DecimalField(max_digits=20, decimal_places=2)
    main_ip = models.GenericIPAddressField()

    billing_type = models.CharField(max_length=1, choices=BILLING_CHOICES, default=MONTHLY)
    purchased_at = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def get_ip(self):
        return self.main_ip

    def total_ip_count(self):
        return self.extra_ip_set.count() + 1

    def get_absolute_url(self):
        return reverse('servers.views.view_server', args=[self.pk])

    def has_notes(self):
        if self.notes == '':
            return False
        return True

    def html_notes(self):
        return '<br />'.join(self.notes.split('\n'))

    def next_due_date(self):
        if self.billing_type == self.MONTHLY:
            test_time = timezone.now().date().replace(day=self.purchased_at.day)
            if test_time < timezone.now().date():
                if test_time.month == 12:
                    test_time = test_time.replace(month=1)
                else:
                    test_time = test_time.replace(month=test_time.month+1)
            return test_time
        else:
            test_time = timezone.now().date().replace(day=self.purchased_at.day, month=self.purchased_at.month)
            if test_time < timezone.now().date():
                test_time = test_time.replace(year=test_time.year+1)
            return test_time

    def percentage_time_used(self):
        next_date = self.next_due_date()
        current_date = timezone.now().date()

        difference = next_date-current_date

        seconds_per_month = 2592000.0
        seconds_per_year = 31536000.0
        if self.billing_type == self.MONTHLY:
            return ((seconds_per_month - difference.total_seconds())/seconds_per_month) * 100.0
        return ((seconds_per_year - difference.total_seconds())/seconds_per_year) * 100.0

    def bar_type(self):
        time_used = self.percentage_time_used()
        prog_type = 'info'
        if time_used >= 30:
            prog_type = 'success'
        if time_used >= 60:
            prog_type = 'warning'
        if time_used >= 80:
            prog_type = 'danger'
        return prog_type


class Extra_IP(models.Model):
    server = models.ForeignKey(Server)
    ip = models.GenericIPAddressField()

    def __unicode__(self):
        return '{} ({})'.format(self.ip, self.server.name)
