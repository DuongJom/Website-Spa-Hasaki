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

@register.filter
def translate_day(value):
    value = value.lower()
    if value == "monday":
        return "Thứ 2"
    elif value == "tuesday":
        return "Thứ 3"
    elif value == "wednesday":
        return "Thứ 4"
    elif value == "thursday":
        return "Thứ 5"
    elif value == "friday":
        return "Thứ 6"
    elif value == "saturday":
        return "Thứ 7"
    else:
        return "Chủ nhật"