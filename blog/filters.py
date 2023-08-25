import django_filters

from blog.models import Like


class LikeFilter(django_filters.FilterSet):
    date_from = django_filters.filters.DateFilter(field_name='date_of_like', lookup_expr='gte')
    date_to = django_filters.filters.DateFilter(field_name='date_of_like', lookup_expr='lte')

    class Meta:
        model = Like
        fields = ('date_from', 'date_to')
