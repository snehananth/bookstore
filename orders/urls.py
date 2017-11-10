from django.conf.urls import url
from .views import SubscribeView, UnSubscribeView

urlpatterns = [
    url(r'^subscribe/$', SubscribeView.as_view()),
    url(r'^unsubscribe/$', UnSubscribeView.as_view()),
]