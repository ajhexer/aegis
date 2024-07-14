import json

from django.test import TestCase
from .models import *
import uuid

from django.contrib.auth.models import User
from openai import OpenAI
from pgvector.django import L2Distance
from django.conf import settings


class ChatBotTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.chatbot = ChatBot.objects.create(
            uuid=uuid.uuid4(),
            name='Test ChatBot',
            user=self.user,
        )
        self.collection = ChatBotCollection.objects.create(
            uuid=uuid.uuid4(),
            chatbot=self.chatbot,
            name='Test Collection'
        )
        self.question_answers = []
        with open("/Users/addez/Dev/interview-chatbot/data.jsonl", "r") as file:
            self.question_answers = [json.loads(i.strip()) for i in file.readlines()[:5]]

        self.system_message = settings.OPENAI_SYSTEM_MESSAGE
        self.delimiter = settings.OPENAI_MESSAGE_DELIMITER
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)

    def test_embedding_similarity(self):
        for question_answer in self.question_answers:
            text = question_answer['question'] + " " + question_answer['doc']
            embedding = self.client.embeddings.create(input=[text], model=settings.OPENAI_EMBEDDING_MODEL).data[0].embedding
            ChatBotEmbedding.objects.create(
                uuid=uuid.uuid4(),
                document=text,
                embedding=embedding,
                collection=self.collection
            )
        embedding = self.client.embeddings.create(input=[self.question_answers[0]["question"]], model=settings.OPENAI_EMBEDDING_MODEL).data[0].embedding
        document = ChatBotEmbedding.objects.order_by(
            L2Distance('embedding', embedding)
        ).first()

        self.assertEqual(document.document, self.question_answers[0]["question"] + " " + self.question_answers[0]["doc"])

    def test_response_from_chatgpt(self):
        user_input = self.question_answers[0]["question"]

        for question_answer in self.question_answers:
            text = question_answer['doc']
            embedding = self.client.embeddings.create(input=[text], model=settings.OPENAI_EMBEDDING_MODEL).data[0].embedding
            ChatBotEmbedding.objects.create(
                uuid=uuid.uuid4(),
                document=text,
                embedding=embedding,
                collection=self.collection
            )

        self.assertIsNotNone(self.chatbot.generate_answer_util(user_input))
