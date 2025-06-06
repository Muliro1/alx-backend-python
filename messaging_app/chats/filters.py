import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.NumberFilter(field_name="sender_id")
    conversation = django_filters.NumberFilter(field_name="conversation_id")
    start_time = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'timestamo', 'sent_at']