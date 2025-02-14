from django import template

register = template.Library()


@register.filter
def round_price(value):
    try:
        value = float(value)
        return int(value) if value.is_integer() else value
    except (ValueError, TypeError):
        return value
