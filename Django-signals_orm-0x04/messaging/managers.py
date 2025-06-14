from django.db import models

class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_read=False)
    
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user).only(
            'id', 'content', 'sender', 'timestamp', 'is_read'
        ) 