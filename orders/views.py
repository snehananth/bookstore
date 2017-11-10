# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from book.models import Book
from member.models import Member
from orders.models import Subscription

# Create your views here.


# STATUS_CODES
INVALID_REQUEST = 101
REQUEST_CANT_BE_SERVED = 201
SERVER_ERROR = 501
SUCCESS = 601


class SubscribeView(View):

    def post(self, request):
        """

        :param request: has all required parameters
        :return: status and message
        example:
        {
            "status": 101,
            "message": "Invalid member id"
        }
        """
        member_id = request.POST.get('member', None)
        book_id = request.POST.get('book', None)
        no_of_copies = request.POST.get('no_of_copies', 1)
        status_dict = {}

        # member id and book id are mandatory to subscribe a book.
        if not member_id or not book_id:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'member id and book id are mandatory'})
            return JsonResponse(status_dict)

        # There should be book and member with the ids specified
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'Book does not exist'})
            return JsonResponse(status_dict)
        except:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'Invalid book id'})
            return JsonResponse(status_dict)
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'Member does not exist'})
            return JsonResponse(status_dict)
        except:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'Invalid member id'})
            return JsonResponse(status_dict)

        # no of copies should be an integer
        try:
            no_of_copies = int(no_of_copies)
        except:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'No of copies should be a number'})
            return JsonResponse(status_dict)

        # if no of books in library should be equal to or more than request for copies
        if book.quantity < no_of_copies:
            status_dict.update({'status': REQUEST_CANT_BE_SERVED, 'message': 'Sorry we dont have required number '
                                                                             'of copies.'})
            return JsonResponse(status_dict)

        # Create a subsription
        obj, created = Subscription.objects.get_or_create(member=member, book=book)
        if created:
            obj.count = no_of_copies
        else:
            obj.count = obj.count + no_of_copies
        obj.save()

        # Decrease the quantity in book
        book.quantity = book.quantity - no_of_copies
        book.save()
        status_dict.update(
            {'status':SUCCESS , 'message': 'Thank you for subscribing'})
        return JsonResponse(status_dict)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SubscribeView, self).dispatch(request, *args, **kwargs)


class UnSubscribeView(View):

    def post(self, request):
        member_id = request.POST.get('member', None)
        book_id = request.POST.get('book', None)
        no_of_copies = request.POST.get('no_of_copies', 1)
        status_dict = {}

        # no of copies should be an integer
        try:
            no_of_copies = int(no_of_copies)
        except:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'No of copies should be a number'})
            return JsonResponse(status_dict)

        # member id and book id are mandatory to subscribe a book.
        if not member_id or not book_id:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'member id and book id are mandatory'})
            return JsonResponse(status_dict)

        # There should be book and member and subscription with the ids specified
        try:
            subscription = Subscription.objects.get(book__id=book_id, member__id=member_id)
        except:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'This member has not borrowed this book'})
            return JsonResponse(status_dict)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'Book does not exist'})
            return JsonResponse(status_dict)
        except:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'Invalid book id'})
            return JsonResponse(status_dict)
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'Member does not exist'})
            return JsonResponse(status_dict)
        except:
            status_dict.update({'status': INVALID_REQUEST, 'message': 'Invalid member id'})
            return JsonResponse(status_dict)

        # if no of books subscribed should be greater or equal to copies returned
        if subscription.count < no_of_copies:
            status_dict.update({'status': REQUEST_CANT_BE_SERVED, 'message': 'No of copies borrowed are less than you '
                                                                             'want to return'})
            return JsonResponse(status_dict)

        # If number of books returned is less than subscribed, deduct it from the count in subscription.
        # If equal, delete the subscription
        if subscription.count > no_of_copies:
            subscription.count = subscription.count - no_of_copies
            subscription.save()
        else:
            subscription.delete()

        # Increase the count of books in library
        book.quantity = book.quantity + no_of_copies
        book.save()
        status_dict.update(
            {'status': SUCCESS, 'message': 'Thank you'})
        return JsonResponse(status_dict)


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UnSubscribeView, self).dispatch(request, *args, **kwargs)