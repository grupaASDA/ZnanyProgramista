from django import template

register = template.Library()

@register.filter
def int_range(value):
    return range(int(value))

@register.filter
def get_rating_stars(value):
    rating_int = int(value)
    return ["⭐" for _ in range(rating_int)] + ["☆" for _ in range(5 - rating_int)]
