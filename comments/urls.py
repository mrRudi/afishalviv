from django.conf.urls import url
from .views import comment_thread, delete


urlpatterns = [
    url(r'^(?P<id>\d+)/$', comment_thread, name='detail'),
    url(r'^(?P<id>\d+)/delete/$', delete, name='delete'),
]
