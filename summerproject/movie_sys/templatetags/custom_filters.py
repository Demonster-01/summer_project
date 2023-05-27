from django import template

register = template.Library()

@register.filter
def includes(value, arg):
    if value is None:
        return False
    return arg in value
