from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    # Example usage of serializers.CharField
    display_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'display_name']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    # Example usage of serializers.SerializerMethodField
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'preview']

    def get_preview(self, obj):
        return obj.message_body[:20]  # First 20 chars as preview

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    # Example usage of serializers.ValidationError
    def validate(self, data):
        if not data.get('participants'):
            raise serializers.ValidationError("A conversation must have at least one participant.")
        return data
