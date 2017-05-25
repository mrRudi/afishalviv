from django.conf.urls import url
from .views import lists,create,detail,update,delete


urlpatterns = [
    url(r'^$', lists, name='list'),
    url(r'^create/$', create, name='create'),
    url(r'^(?P<slug>[^\/]+)/$', detail, name='detail'),
    url(r'^(?P<slug>[^\/]+)/edit/$', update, name='update'),
    url(r'^(?P<slug>[^\/]+)/delete/$', delete, name='delete'),


]
