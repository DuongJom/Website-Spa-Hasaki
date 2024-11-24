from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    """
    Usage: {{ request.path|startswith:"/admin/" }}
    Checks if 'value' (the string) starts with 'arg'.
    """
    return value.startswith(arg)

@register.filter
def phoneformat(value, arg):
    if not value.startswith("0") or len(value) == int(arg) - 1:
        return "0" + value
    return value