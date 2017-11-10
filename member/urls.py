from django.conf.urls import url
from .views import MemberList, MemberDetail

urlpatterns = [
    url(r'^member/$', MemberList.as_view()),
    url(r'^memberupdate/(?P<id>[0-9]+)/$', MemberDetail.as_view()),
]