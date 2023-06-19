from django.utils import timezone

from django import template

register = template.Library()


@register.filter
def duration_format(value):
    if value is None:
        return ""  # or any other default value

    hours = value // 3600
    minutes = (value % 3600) // 60
    seconds = value % 60

    duration_string = ""
    if hours > 0:
        duration_string += '{}h '.format(hours)
    if minutes > 0 or hours > 0:
        duration_string += '{}m '.format(minutes)
    duration_string += '{}s'.format(seconds)

    return duration_string


@register.filter
def datetime_format(datetime):
    if datetime is not None:
        datetime_with_timezone = timezone.localtime(datetime)
        formatted_datetime = datetime_with_timezone.strftime("%B %d, %Y, %H:%M:%S")
        return f"{formatted_datetime}"
    else:
        return ''
