# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Member
from django.views.decorators.csrf import csrf_exempt
from .serializers import MemberSerializer
# Create your views here.


class MemberList(APIView):
    """
    View to get all the members and add members
    """

    def get(self, request):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        """

        :param request:
        :return: data if its valid else standard error codes to specify the erros
        """
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetail(APIView):
        """
        This View is to look up a member, update and delete the member
        """

        def get_object(self, id):
            try:
                return Member.objects.get(id=id)
            except Member.DoesNotExist:
                raise Http404

        def get(self, request, id):
            """

            :param id:id of member
            :return: member json if exists. //This can be modified to search on any other field
            """
            member = self.get_object(id)
            serializer = MemberSerializer(member)
            return Response(serializer.data)

        def put(self, request, id):
            """
            This is for updating a member
            :param request:
            :param id: id of memebr
            :return:
            """
            member = self.get_object(id)
            serializer = MemberSerializer(member, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, id):
            """

            :param request:
            :param id: id of member to delete
            :return: status of delete operation
            """
            member = self.get_object(id)
            member.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)