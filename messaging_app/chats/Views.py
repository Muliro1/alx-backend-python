from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message

class MessageListView(APIView):
    """
    View to list messages for a conversation.
    """

    def get(self, request, conversation_id):
        # Example: Only allow participants to view messages
        if not request.user.is_authenticated or not request.user.is_participant(conversation_id):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        messages = Message.objects.filter(conversation_id=conversation_id)
        # Serialize messages as needed
        # serializer = MessageSerializer(messages, many=True)
        # return Response(serializer.data)
        return Response({'count': messages.count()}) 
