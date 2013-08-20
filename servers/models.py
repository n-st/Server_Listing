from django.db import models
from django.utils import timezone


class Server(models.Model):
    name = models.CharField(max_length=255)
    notes = models.TextField()

    cost = models.DecimalField(max_digits=20, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
