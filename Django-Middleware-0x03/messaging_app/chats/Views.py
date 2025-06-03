from rest_framework import viewsets
from chats.models import Message
from chats.serializers import MessageSerializer
from chats.permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
