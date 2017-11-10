# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class BaseModel(models.Model):
    """
    This is the base class which has to be inherited by all classes who want to capture created_on and updated_on time
    """
    created_on = models.DateTimeField(editable=False, auto_now=True)
    updated_on = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True