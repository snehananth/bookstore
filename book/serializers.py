from rest_framework import serializers
from .models import Book

import datetime


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Book
        fields = ('id', 'name', 'author', 'mrp', 'sale_price', 'isbn', 'is_available', 'quantity','created_on', 'updated_on')
        read_only_fields = ('created_on', 'updated_on')