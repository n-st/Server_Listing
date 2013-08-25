from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from datetime import timedelta
from ping import Ping
from django.conf import settings
from servers.emailers import send_failure, send_back_up
from servers.solusapi import SolusAPI as SolusConnectorAPI


class Purpose(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='', blank=True)
    purpose_website = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Server(models.Model):

    MONTHLY = 'm'
    YEARLY = 'y'

    BILLING_CHOICES = (
        (MONTHLY, 'Monthly'),
        (YEARLY, 'Yearly'),
    )

    OPENVZ = 'o'
    KVM = 'k'

    VIRT_TYPES = (
        (OPENVZ, 'OpenVZ'),
        (KVM, 'KVM'),
    )

    name = models.CharField(max_length=255)
    notes = models.TextField(default='', blank=True)
    purposes = models.ManyToManyField(Purpose, blank=True, null=True)

    cost = models.DecimalField(max_digits=20, decimal_places=2)
    main_ip = models.GenericIPAddressField()

    # Server details
    number_cores = models.IntegerField(default=1)
    bandwidth = models.IntegerField(default=0)
    ram = models.IntegerField(default=0)
    burst = models.IntegerField(default=0)
    hdd_space = models.IntegerField(default=0)
    virt_type = models.CharField(max_length=1, choices=VIRT_TYPES, default=OPENVZ)

    billing_type = models.CharField(max_length=1, choices=BILLING_CHOICES, default=MONTHLY)
    purchased_at = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    check_status = models.BooleanField(default=True)


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

    def is_up(self):
        if self.check_status is False:
            return False
        if ServerCheck.objects.filter(server=self).exists():
            return ServerCheck.objects.filter(server=self).latest('check_date').online
        return False

    def time_since_last_change(self):
        if self.check_status is False:
            return False
        if ServerCheck.objects.filter(server=self).exists():
            return ServerCheck.objects.filter(server=self, did_change=True).latest('check_date').check_date
        return timezone.now()

    def has_uptime_history(self):
        return ServerCheck.objects.filter(server=self, did_change=True).exists()

    def uptime_history(self):
        return ServerCheck.objects.filter(server=self, did_change=True).order_by('-check_date')

    def last_checked(self):
        return ServerCheck.objects.filter(server=self).latest('check_date').check_date

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

    def has_purpose(self):
        if self.purposes.count() > 0:
            return True
        return False


class Extra_IP(models.Model):
    server = models.ForeignKey(Server)
    ip = models.GenericIPAddressField()

    def __unicode__(self):
        return '{} ({})'.format(self.ip, self.server.name)


class ServerCheck(models.Model):
    server = models.ForeignKey(Server)
    ip_address = models.GenericIPAddressField()
    check_date = models.DateTimeField()

    online = models.BooleanField(default=True)
    did_change = models.BooleanField(default=False)
    last_change = models.ForeignKey('ServerCheck', null=True, blank=True)

    def server_name(self):
        return self.server.name

    @classmethod
    def check_server(cls, server):

        # Check if there was another in the leeway time
        minimum_time = timezone.now()-timedelta(minutes=settings.LEEWAY_TIME)
        if ServerCheck.objects.filter(server=server, check_date__gte=minimum_time).count() > 0:
            return False

        check_log = ServerCheck(server=server, ip_address=server.main_ip, check_date=timezone.now())
        checker = Ping(check_log.ip_address).run_ping()
        check_log.online = checker.is_online

        check_log.save()
        if check_log.did_change:
            if checker.is_online:
                send_back_up(checker, check_log)
            else:
                send_failure(checker, check_log)
        return check_log

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if ServerCheck.objects.filter(server=self.server, check_date__lt=self.check_date).exists():
            if self.online == ServerCheck.objects.filter(
                    server=self.server,
                    check_date__lt=self.check_date
            ).latest('check_date').online:
                self.did_change = False
            else:
                self.did_change = True
        else:
            self.did_change = True

        if ServerCheck.objects.filter(server=self.server, did_change=True, check_date__lt=self.check_date).exists():
            self.last_change = ServerCheck.objects.filter(
                server=self.server,
                did_change=True,
                check_date__lt=self.check_date
            ).latest('check_date')

        return super(ServerCheck, self).save(force_insert, force_update, using, update_fields)

    def __unicode__(self):
        if self.online:
            online_text = 'Online'
        else:
            online_text = 'Offline'
        return online_text + ' ' + unicode(self.check_date)

    def abstracted_time_relative_to_now(self):
        checks = ServerCheck.objects.filter(
            server=self.server,
            did_change=True,
            check_date__gt=self.check_date
        ).order_by('check_date')
        if checks.exists():
            next_check = checks[0]
            delta_time = next_check.check_date - self.check_date
            return timezone.now() - delta_time
        else:
            return self.check_date


class SolusAPI(models.Model):
    api_url = models.URLField()
    api_key = models.CharField(max_length=255)
    api_hash = models.CharField(max_length=255)
    server = models.OneToOneField(Server)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_ip_list(self):
        api = SolusConnectorAPI(
            url=self.api_url,
            api_key=self.api_key,
            api_hash=self.api_hash
        )

        ips = api.get_ips()
        if ips:
            current_ip_list = [self.server.main_ip]
            for ip in self.server.extra_ip_set.all():
                current_ip_list.append(ip.ip)

            for ip in ips:
                if ip in current_ip_list:
                    continue
                else:
                    Extra_IP(ip=ip, server=self.server).save()
            return True
        return False
