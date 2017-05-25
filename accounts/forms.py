from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    logout as dj_logout,
    login as dj_login
)

from django.contrib.auth.models import User


class UserLoginForms(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args,**kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exits')
            if (not user.is_active) or (not user.check_password(password)):
                raise forms.ValidationError('Incorrect name/password')

        return super(UserLoginForms, self).clean(*args,**kwargs)


class UserRegisterForms(forms.ModelForm):
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Password must match')

        return super(UserRegisterForms, self).clean(*args,**kwargs)


