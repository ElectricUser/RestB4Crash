from django.utils import timezone

from django import template

register = template.Library()


@register.filter
def duration_format(value):
    if value is None:
        return ""  # or any other default value

    return format_duration(value)


@register.filter
def datetime_format(datetime):
    if datetime is not None:
        datetime_with_timezone = timezone.localtime(datetime)
        formatted_datetime = datetime_with_timezone.strftime("%d %B %Y, %H:%M:%S")
        return f"{formatted_datetime}"
    else:
        return ''


@register.filter
def pause_duration_format(value):
    if value is None:
        return "No Pauses"  # or any other default value

    return format_duration(value)


def format_duration(value):
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
def default_value(value):
    return value if (value is not None and value != '') else 0
