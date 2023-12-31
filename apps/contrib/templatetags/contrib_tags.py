import re
import unicodedata

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.forms.utils import flatatt
from django.template import defaultfilters
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def include_template_string(template, **kwargs):
    rendered_template = render_to_string(template, kwargs)
    return str(rendered_template)


@register.simple_tag
def combined_url_parameter(request_query_dict, **kwargs):
    combined_query_dict = request_query_dict.copy()
    for key in kwargs:
        combined_query_dict.setlist(key, [kwargs[key]])
    encoded_parameter = "?" + combined_query_dict.urlencode()
    return encoded_parameter


@register.simple_tag
def filter_has_perm(perm, user, objects):
    """Filter a list of objects based on user permissions."""
    if not hasattr(user, "has_perm"):
        # If the swapped user model does not support permissions, all objects
        # will be returned. This is taken from rules.templatetags.has_perm.
        return objects
    else:
        return [obj for obj in objects if user.has_perm(perm, obj)]


@register.simple_tag()
def html_date(value, displayfmt=None, datetimefmt="c", **kwargs):
    """Format a date and wrap it in a html <time> element.

    Additional html attributes may be provided as kwargs (e.g. 'class').

    Note: Converts the value to localtime as we loose the expects_localtime
    flag functionality by directly calling the date filter from django.
    """
    if value:
        localtime_value = timezone.localtime(value)
        displaydate = defaultfilters.date(localtime_value, displayfmt)
        datetime = defaultfilters.date(localtime_value, datetimefmt)
        attribs = flatatt(kwargs)
        result = '<time %s datetime="%s">%s</time>' % (attribs, datetime, displaydate)
        return mark_safe(result)


@register.filter
def classify(value):
    """
    Create a valid CSS class name from a value.

    Converts to ASCII. Converts spaces to dashes. Removes characters that
    aren't alphanumerics, underscores, or hyphens.
    Also strips leading and trailing whitespace.
    """
    if value is None:
        return "NONE"

    value = force_str(value)
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value).strip()
    return mark_safe(re.sub(r"[-\s]+", "-", value))


@register.filter
def fa_class(icon):
    if hasattr(icon, "startswith") and not icon.startswith("fa"):
        return "fas fa-{icon}".format(icon=icon)
    return icon


@register.simple_tag()
def matomo_enabled():
    if hasattr(settings, "MATOMO_ENABLED"):
        return settings.MATOMO_ENABLED
    return False


@register.inclusion_tag("a4_candy_contrib/matomo/tracking_code.html")
def matomo_tracking_code():
    if not hasattr(settings, "MATOMO_SITE_ID"):
        raise ImproperlyConfigured("MATOMO_SITE_ID does not exist.")

    if not hasattr(settings, "MATOMO_URL"):
        raise ImproperlyConfigured("MATOMO_URL does not exist.")

    cookie_disabled = False
    if hasattr(settings, "MATOMO_COOKIE_DISABLED"):
        cookie_disabled = settings.MATOMO_COOKIE_DISABLED

    return {
        "id": settings.MATOMO_SITE_ID,
        "url": settings.MATOMO_URL,
        "cookie_disabled": cookie_disabled,
    }


@register.filter
def devide(value, arg):
    if arg:
        return round(value / arg, 2)
    return 0
