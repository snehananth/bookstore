# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models



from base.models import BaseModel
# Create your models here.

class Member(BaseModel):
    email = models.EmailField(_('Email Address'), unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    city_name = models.CharField(max_length=30, blank=True, null=True)
    mobile_no = models.IntegerField(max_length=10)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
