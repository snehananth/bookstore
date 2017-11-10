# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from base.models import BaseModel


class Book(BaseModel):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    mrp = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    isbn = models.IntegerField(max_length=14)
    is_available = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)

    objects = models.Manager()
