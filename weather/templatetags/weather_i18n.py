from django.utils.translation import gettext_lazy as _
from django import template

register = template.Library()

def t(value):
    return _(value)

register.filter("t", t)
