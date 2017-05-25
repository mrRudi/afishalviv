"""kursach URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from forum.views import Home
# from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^event/', include('forum.urls')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^markdownx/', include('markdownx.urls')),

    url(r'^post/', include('posts.urls', namespace='posts')),
    url(r'^comment/', include('comments.urls', namespace='comments')),

    url(r'^auth/', include('accounts.urls', namespace='register')),

    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # url(r'', include('my_authorization.urls', namespace='myauthorization'),),
    url(r'', include('my_authorization.urls', ),),

    # url(r'^login/$', auth_views.login, name='login'),
    # url(r'^logout/$', auth_views.logout, name='logout'),
    # url(r'', include('mysite.urls')),
]
