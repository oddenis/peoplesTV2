from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
    vals = 0
    if val == 3:
        vals = 1
    else:
        vals = int(val) + 1
    return vals