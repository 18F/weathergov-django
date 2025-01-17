from django.utils.translation import gettext as _
from django import template

register = template.Library()

def t(value):
    return value

register.filter("t", t)
