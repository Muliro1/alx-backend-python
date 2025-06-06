from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import filters 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        if not participants:
            return Response({'error': 'Participants required.'}, status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')
        if not (conversation_id and sender_id and message_body):
            return Response({'error': 'conversation, sender, and message_body are required.'}, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.create(
            conversation_id=conversation_id,
            sender_id=sender_id,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], url_path='by-conversation/(?P<conversation_id>[^/.]+)')
    def list_by_conversation(self, request, conversation_id=None):
        # Check if user is a participant of the conversation
        conversation = Conversation.objects.filter(id=conversation_id, participants=request.user).first()
        if not conversation:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        messages = Message.objects.filter(conversation_id=conversation_id)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
