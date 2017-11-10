# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from book.models import Book
import datetime
from member.models import Member
from base.models import BaseModel
# Create your models here.


class Subscription(BaseModel):
    member = models.ForeignKey(Member)
    book = models.ForeignKey(Book)
    count = models.IntegerField(default=1)