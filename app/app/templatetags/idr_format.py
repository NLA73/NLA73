from django import template

register = template.Library()

@register.filter(name='idrformat')
def idrformat(value):
    try:
        if value is None or value == "":
            return "0"
        # Menghapus desimal dan format ke ribuan dengan titik
        value = int(float(value))
        return "{:,}".format(value).replace(",", ".")
    except (ValueError, TypeError):
        return value