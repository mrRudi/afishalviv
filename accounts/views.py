from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    logout as dj_logout,
    login as dj_login
)
from django.urls import reverse

from .forms import UserLoginForms, UserRegisterForms


def login(request):
    form = UserLoginForms(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        dj_login(request, user)
        return HttpResponseRedirect(reverse('posts:list'))

    context = {
        'form':form,
        'title':'login',
    }
    return render(request, "accounts/form.html",context)


def logout(request):
    dj_logout(request)
    return HttpResponseRedirect(reverse('posts:list'))


def register(request):
    form = UserRegisterForms(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        dj_login(request, new_user)
        return HttpResponseRedirect(reverse('posts:list'))

    context = {
        'form': form,
        'title': 'register',
    }
    return render(request, "accounts/form.html", context)