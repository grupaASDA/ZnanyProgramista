from django import template

register = template.Library()

@register.filter
def int_range(value):
    return range(int(value))

@register.filter
def get_rating_stars(value):
    rating_float = float(value)  # Convert to float for more precise calculations
    full_stars = int(rating_float)  # Number of full stars
    half_stars = round((rating_float - full_stars) * 2)  # Number of half stars (rounded)
    empty_stars = 5 - full_stars - half_stars  # Number of empty stars

    stars = ["⭐" for _ in range(full_stars)]  # Add full stars
    if half_stars == 1:  # Add half star if needed
        stars.append("½⭐")
    stars.extend(["☆" for _ in range(empty_stars)])  # Add empty stars
    return stars
