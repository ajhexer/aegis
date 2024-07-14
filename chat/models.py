from django.db import models
from core.models import ChatBot
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Conversation(models.Model):
    chatbot = models.ForeignKey(ChatBot, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    timestamp = models.DateTimeField(auto_now_add=False, default=timezone.now)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4())

    def __str__(self):
        return self.title


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', to_field="uuid")
    user_input = models.TextField()
    model_answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message in {self.conversation.title}'

    class Meta:
        ordering = ['timestamp']
