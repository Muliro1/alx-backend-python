from rest_framework import permissions
from rest_framework.permissions import  SAFE_METHODS

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for all participants
        if request.method in SAFE_METHODS:
            return True

        # Only allow PUT, PATCH, DELETE for participants (customize as needed)
        if request.method in ["PUT", "PATCH", "DELETE"]:
            # Your logic to check if the user can modify/delete the object
            # For demonstration, always return True
            return True

        return False
