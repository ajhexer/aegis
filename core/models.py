from django.db import models
from pgvector.django import VectorField
from django.contrib.auth.models import User
from django.conf import settings
from openai import OpenAI
from pgvector.django import L2Distance
from .utils import generate_answer_util
from django.core.exceptions import ObjectDoesNotExist



class ChatBot(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatbots')

    def generate_answer(self, user_input):
        client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)
        related_doc = self.__get_related_doc(user_input, client)
        return generate_answer_util(user_input, settings.OPENAI_SYSTEM_MESSAGE, settings.OPENAI_MESSAGE_DELIMITER, settings.OPENAI_GENERATION_MODEL, related_doc, client)

    def __get_related_doc(self, user_input, client):
        embedding = client.embeddings.create(input=[user_input], model=settings.OPENAI_EMBEDDING_MODEL).data[0].embedding
        collections = self.collections.all()
        try:
            related_doc = ChatBotEmbedding.objects.filter(collection__in=collections).order_by(L2Distance('embedding', embedding)).all()
            related_doc = related_doc[:min(3, len(related_doc))]
        except ObjectDoesNotExist:
            related_doc = None

        return related_doc


class ChatBotCollection(models.Model):
    uuid = models.UUIDField(primary_key=True)
    chatbot = models.ForeignKey(ChatBot, on_delete=models.CASCADE, related_name='collections', to_field="uuid")
    name = models.CharField(max_length=255, blank=True, null=True)


class ChatBotEmbedding(models.Model):
    uuid = models.UUIDField(primary_key=True)
    collection = models.ForeignKey(ChatBotCollection, models.CASCADE, related_name='embeddings', to_field="uuid")
    embedding = VectorField(dimensions=1536)
    document = models.TextField()


    