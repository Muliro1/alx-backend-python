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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_messages(request):
    filters = {}
    conversation_id = request.query_params.get('conversation_id')
    sender_id = request.query_params.get('sender_id')
    receiver_id = request.query_params.get('receiver_id')
    parent_message_id = request.query_params.get('parent_message_id')
    unread_only = request.query_params.get('unread_only', 'false').lower() == 'true'

    if unread_only:
        messages = Message.unread.unread_for_user(request.user)
    else:
        if conversation_id:
            filters['conversation_id'] = conversation_id
        if sender_id:
            filters['sender_id'] = sender_id
        if receiver_id:
            filters['receiver_id'] = receiver_id
        if parent_message_id:
            filters['parent_message_id'] = parent_message_id

        messages = Message.objects.filter(**filters)\
            .select_related('sender', 'receiver', 'edited_by', 'parent_message')\
            .only(
                'id', 'content', 'sender', 'receiver', 'timestamp',
                'edited', 'edited_by', 'parent_message', 'is_read'
            )

    data = [
        {
            'id': msg.id,
            'content': msg.content,
            'sender': str(msg.sender),
            'receiver': str(msg.receiver),
            'timestamp': msg.timestamp,
            'edited': msg.edited,
            'edited_by': str(msg.edited_by) if msg.edited_by else None,
            'parent_message': msg.parent_message.id if msg.parent_message else None,
            'is_read': msg.is_read
        }
        for msg in messages
    ]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_message(request):
    data = request.data
    receiver = data.get('receiver')
    content = data.get('content')
    conversation = data.get('conversation')
    parent_message = data.get('parent_message')
    if not receiver or not content:
        return Response({'detail': 'receiver and content are required.'}, status=status.HTTP_400_BAD_REQUEST)

    message = Message(
        receiver_id=receiver,
        content=content,
    )
    message.sender = request.user
    if conversation:
        message.conversation_id = conversation
    if parent_message:
        message.parent_message_id = parent_message
    message.save()
    return Response({
        'id': message.id,
        'content': message.content,
        'sender': str(message.sender),
        'receiver': str(message.receiver),
        'timestamp': message.timestamp,
        'edited': message.edited,
        'edited_by': str(message.edited_by) if message.edited_by else None,
        'parent_message': message.parent_message.id if message.parent_message else None
    }, status=status.HTTP_201_CREATED)
