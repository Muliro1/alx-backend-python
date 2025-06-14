from django.db import models

class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_read=False)
    
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user).only(
            'id', 'content', 'sender', 'timestamp', 'is_read'
        )
    
    def unread_for_user(self, user):
        """
        Returns unread messages for a specific user.
        This is an alias for for_user() for backward compatibility.
        """
        return self.for_user(user) 