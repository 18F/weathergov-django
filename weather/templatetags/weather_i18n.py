import json
from django.utils.translation import gettext_lazy as _
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def t(value, args=False):
    if(args):
        args_parsed = json.loads(args)
        translated = _(value)
        result = translated
        for key,val in args_parsed:
            result = result.replace(key, val)
        return result
    return _(value)

def json_encode(value):
    if(isinstance(value, dict)):
        return mark_safe(json.dumps(value))
    return ""

def normalize_wfo(value):
    anchorage_alternates = ["alu", "aer"]
    if value.lower() in anchorage_alternates:
        return "AFC"
    return value

@register.simple_tag
def trans_with_args(value, *args, **kwargs):
    translated = _(value)
    return mark_safe(
        translated.format(**kwargs)
    )


register.filter("t", t)
register.filter("json_encode", json_encode)
register.filter("normalize_wfo", normalize_wfo)
