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
    purchased_at = models.DateTimeField(default=timezone.now)
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
        print self.purchased_at.day
        test_time = timezone.now().replace(day=self.purchased_at.day)
        if test_time < timezone.now():
            if test_time.month == 12:
                test_time = test_time.replace(month=1)
            else:
                test_time = test_time.replace(month=test_time.month+1)
        return test_time


class Extra_IP(models.Model):
    server = models.ForeignKey(Server)
    ip = models.GenericIPAddressField()
