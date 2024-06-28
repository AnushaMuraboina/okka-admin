from django import template
from django.utils import timezone
from datetime import datetime, date

register = template.Library()

@register.filter(name='time_since_review')
def timesince_custom(value):
    if not value:
        return ""

    now = timezone.now()

    # Ensure value is timezone-aware
    if isinstance(value, date) and not isinstance(value, datetime):
        value = datetime.combine(value, datetime.min.time())
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())

    diff = now - value

    if diff.days >= 365:
        years = diff.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif diff.days >= 30:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif diff.days >= 1:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"


@register.filter(name='stars')
def stars(rating_value):
    full_star = '<i class="fa-solid fa-star"></i>'
    empty_star = '<i class="fa-regular fa-star"></i>'  # Use fa-regular for empty star
    full_stars_html = full_star * rating_value
    empty_stars_html = empty_star * (5 - rating_value)
    return full_stars_html + empty_stars_html