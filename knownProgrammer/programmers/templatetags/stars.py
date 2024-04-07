from django import template
from django.templatetags.static import static

register = template.Library()


@register.filter
def int_range(value):
    return range(int(value))


@register.filter
def get_rating_stars(value):
    rating_float = float(value)
    full_stars = int(rating_float)
    half_stars = round((rating_float - full_stars) * 2)
    empty_stars = 5 - full_stars - half_stars
    stars = []

    for _ in range(full_stars):
        stars.append(f'<img width="30" height="30" src="{static("images/star-full.png")}" alt="star-full">')

        # Add half star if needed
    if half_stars == 1:
        stars.append(f'<img width="30" height="30" src="{static("images/star-half.png")}" alt="star-half-empty">')

        # Add empty stars
    for _ in range(empty_stars):
        stars.append(f'<img width="30" height="30" src="{static("images/star-empty.png")}" alt="star-empty">')

    return ''.join(stars)
