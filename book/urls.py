from django.conf.urls import url
from .views import BookDetail,BookListView

urlpatterns = [
    url(r'^book/$', BookListView.as_view()),
    url(r'^bookupdate/(?P<id>[0-9]+)/$', BookDetail.as_view()),
]