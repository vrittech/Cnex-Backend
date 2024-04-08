# filters.py
import django_filters
from .models import Notification

class CustomFilter(django_filters.FilterSet):
    notification_type = django_filters.CharFilter(method='filter_notification_type')

    class Meta:
        model = Notification
        fields = ['notification_type','is_read']

    def filter_notification_type(self, queryset,name, values):
        return queryset.filter(notification_type__in=self.request.GET.getlist('notification_type'))
