from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget
from markdownx.fields import MarkdownxFormField


BIRTH_YEAR_CHOICES = ('2015', '2016', '2017')


class PostForms(forms.ModelForm):

    content = forms.CharField(widget=PagedownWidget(show_preview=False), label='Контент')
    # myfield = MarkdownxFormField()
    publish = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES), label='Дата')

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            # 'myfield',
            'image',
            'draft',
            'publish',
            'ART',
            'MUSIC',
            'CINEMA',
            'THEATER',
            'LITERATURE',
            'SPORT',
            'NIGHTLIFE',
            'FESTIVALS',
            'TEACHING',
            'BUSINESS',
            'EXCURSIONS',
            'OTHER',
        ]