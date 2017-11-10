# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from .models import Member


class ViewTestCase(TestCase):
    """Test suite for the member views."""

    def setUp(self):
        self.client = APIClient()
        self.member_data = {'first_name': 'Sneha'}
        self.response = self.client.post(
            reverse('create'),
            self.member_data,
            format="json")


    def test_api_can_create_a_member(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)