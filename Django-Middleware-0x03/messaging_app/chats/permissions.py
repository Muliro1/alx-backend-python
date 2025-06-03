from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Assuming obj is a Message instance with a .conversation field
        # and Conversation has a participants ManyToMany field
        return request.user in obj.conversation.participants.all()
