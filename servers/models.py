from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from datetime import timedelta
from ping import Ping
from django.conf import settings
from servers.emailers import send_failure, send_back_up
from servers.solusapi import SolusAPI as SolusConnectorAPI
from servers.responder_api import ResponderAPI as ResponderConnectorAPI


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
    next_due_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    check_status = models.BooleanField(default=True)
    last_checked = models.DateTimeField(default=timezone.now)

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

    def percentage_time_used(self):
        next_date = self.next_due_date
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
            return ServerCheck.objects.filter(server=self).latest('check_date').check_date
        return timezone.now()

    def has_uptime_history(self):
        return ServerCheck.objects.filter(server=self).exists()

    def uptime_history(self):
        return ServerCheck.objects.filter(server=self).order_by('-check_date')

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

    def has_solus(self):
        if self.solusapi is not None:
            return True
        return False

    def has_responder(self):
        if self.responderapi is not None:
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
    last_change = models.ForeignKey('ServerCheck', null=True, blank=True)

    def server_name(self):
        return self.server.name

    @classmethod
    def check_server(cls, server):
        check_log = ServerCheck(server=server, ip_address=server.main_ip, check_date=timezone.now())
        checker = Ping(check_log.ip_address).run_ping()
        check_log.online = checker.is_online

        if ServerCheck.objects.filter(server=server).exists():
            last_check = ServerCheck.objects.filter(server=server).order_by('-id')[0]
            if check_log.online == last_check.online:
                # The server status did not change
                return last_check
        else:
            last_check = None

        server.last_checked = timezone.now()
        server.save()

        check_log.last_change = last_check

        if check_log.online:
            send_back_up(checker, check_log)
        else:
            send_failure(checker, check_log)

        check_log.save()
        return check_log

    def __unicode__(self):
        if self.online:
            online_text = 'Online'
        else:
            online_text = 'Offline'
        return online_text + ' ' + unicode(self.check_date)

    def abstracted_time_relative_to_now(self):
        checks = ServerCheck.objects.filter(
            server=self.server,
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

    def update_bandwidth(self):
        api = SolusConnectorAPI(
            url=self.api_url,
            api_key=self.api_key,
            api_hash=self.api_hash
        )

        bandwidth = api.get_bandwidth()
        if bandwidth:
            self.server.bandwidth = bandwidth["total"]
            self.server.save()
            return self.server.bandwidth
        return False

    def update_ram(self):
        api = SolusConnectorAPI(
            url=self.api_url,
            api_key=self.api_key,
            api_hash=self.api_hash
        )

        memory = api.get_memory()
        if memory:
            self.server.ram = memory["total"]
            self.server.save()
            return self.server.ram
        return False

    def update_hdd(self):
        api = SolusConnectorAPI(
            url=self.api_url,
            api_key=self.api_key,
            api_hash=self.api_hash
        )

        hdd = api.get_hdd()
        if hdd:
            self.server.hdd_space = hdd["total"]
            self.server.save()
            return self.server.hdd_space
        return False

    def get_raw_api(self):
        api = SolusConnectorAPI(
            url=self.api_url,
            api_key=self.api_key,
            api_hash=self.api_hash
        )
        return api


class ResponderAPI(models.Model):
    api_url = models.GenericIPAddressField()
    api_key = models.CharField(max_length=255)
    api_port = models.IntegerField(max_length=8)
    server = models.OneToOneField(Server)

    def get_responder_data(self):
        return ResponderConnectorAPI(self.api_key, self.api_url, self.api_port).send_request()
