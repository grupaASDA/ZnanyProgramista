import django_filters
from .models import ProgrammerProfile



class ProgrammerFilter(django_filters.FilterSet):
    wage = django_filters.RangeFilter()
    first_name = django_filters.CharFilter(field_name='user_id__first_name', lookup_expr="contains")
    last_name = django_filters.CharFilter(field_name='user_id__last_name', lookup_expr="contains")

    class Meta:
        model = ProgrammerProfile
        fields = {
            'experience': ['exact'],
            'programming_languages': ['contains'],
            'tech_stack': ['contains']
        }