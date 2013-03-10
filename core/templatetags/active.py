from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def active(request, url):
    if reverse(url) == request.path:
        return 'active'
    else:
        return ''
