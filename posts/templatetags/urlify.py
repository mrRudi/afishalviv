from django import template
from django.template.defaultfilters import stringfilter
from django.utils.http import urlquote, urlquote_plus

register = template.Library()


@register.filter(name="urlify")
@stringfilter
def urlify(value):
    return urlquote_plus(value)


black_star = u"\u2605"
white_star = u"\u2606"


@register.filter(name="star")
def star(number_black):
    return black_star*number_black + white_star*(5-number_black)