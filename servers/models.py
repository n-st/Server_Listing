from django.db import models
from django.utils import timezone


class Server(models.Model):
    name = models.CharField(max_length=255)
    notes = models.TextField(default='', blank=True)

    cost = models.DecimalField(max_digits=20, decimal_places=2)
    main_ip = models.GenericIPAddressField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def get_ip(self):
        return self.main_ip


class Extra_IP(models.Model):
    server = models.ForeignKey(Server)
    ip = models.GenericIPAddressField()
