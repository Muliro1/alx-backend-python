from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Message
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete_user(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({'detail': 'User account deleted.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_threaded_conversation(request, message_id):
    try:
        message = Message.objects.select_related('sender', 'receiver', 'edited_by', 'parent_message')\
            .prefetch_related('replies', 'history', 'notifications').get(pk=message_id)
    except Message.DoesNotExist:
        return Response({'detail': 'Message not found.'}, status=status.HTTP_404_NOT_FOUND)

    def get_replies(msg):
        replies = msg.replies.all().select_related('sender', 'receiver', 'edited_by', 'parent_message').prefetch_related('replies')
        return [
            {
                'id': reply.id,
                'content': reply.content,
                'sender': str(reply.sender),
                'timestamp': reply.timestamp,
                'edited': reply.edited,
                'edited_by': str(reply.edited_by) if reply.edited_by else None,
                'replies': get_replies(reply)
            }
            for reply in replies
        ]

    data = {
        'id': message.id,
        'content': message.content,
        'sender': str(message.sender),
        'timestamp': message.timestamp,
        'edited': message.edited,
        'edited_by': str(message.edited_by) if message.edited_by else None,
        'replies': get_replies(message)
    }
    return Response(data)
