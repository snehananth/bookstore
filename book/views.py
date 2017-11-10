# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import json
from rest_framework.views import APIView
from .models import Book
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .serializers import BookSerializer
from rest_framework import status
from django.http import Http404
# Create your views here.


class BookListView(APIView):
    """
    View to get all the books and add book
    """

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        """

        :param request:
        :return: book data if its valid else standard error codes to specify the erros
        """
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
        """
        This View is to look up a book, update and delete the book
        """

        def get_object(self, id):
            try:
                return Book.objects.get(id=id)
            except Book.DoesNotExist:
                raise Http404

        def get(self, request, id):
            """

            :param id:id of book
            :return: book object if exists. //This can be modified to search on any other field
            """
            book = self.get_object(id)
            serializer = BookSerializer(book)
            return Response(serializer.data)

        def put(self, request, id):
            """
            This is for updating a book
            :param request:
            :param id: id of book
            :return:
            """
            book = self.get_object(id)
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, id):
            """

            :param request:
            :param id: id of book to delete
            :return: status of delete operation
            """
            book = self.get_object(id)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)