from django import template

register = template.Library()


@register.filter
def current_user(instance, date):
    """
    allows only one argument for one exact method
    """
    return instance.current_user(date)
