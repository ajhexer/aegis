
from celery import shared_task
from .models import ChatBot, ChatBotCollection, ChatBotEmbedding
import PyPDF2
from django.shortcuts import get_object_or_404
from openai import OpenAI
import uuid
import os
from django.conf import settings


def data_extract(document, name, chatbot_uuid):
    chatbot = get_object_or_404(ChatBot, uuid=chatbot_uuid)

    chatbot_collection = ChatBotCollection.objects.create(
        uuid=uuid.uuid4(),
        name=name,
        chatbot=chatbot
    )
    file_extension = os.path.splitext(document.name)[1].lower()

    if file_extension == '.txt':
        text = document.read()
    elif file_extension == '.pdf':
        pdf = PyPDF2.PdfReader(document)
        text = ""
        for page in range(len(pdf.pages)):
            text += pdf.pages[page].extract_text()
    else:
        raise Exception("File format is not supported")
    process_document.delay(text, chatbot_collection.uuid)



@shared_task
def process_document(document, chatbot_collection_uuid):
    text = document.split()
    length = len(text)
    chunks = [text[i:min(i+800, length)] for i in range(0, len(text), 800)]
    embed_document.delay(chunks, chatbot_collection_uuid)



@shared_task
def embed_document(chunks, chatbot_collection_uuid, embed_model="text-embedding-ada-002"):
    for chunk in chunks:
        text = ' '.join([str(x) for x in chunk if x != ' '])
        ingest_embedding.delay(text, chatbot_collection_uuid, embed_model)

@shared_task
def ingest_embedding(chunk, chatbot_collection_uuid, embed_model="text-embedding-ada-002"):
    client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)
    embedding = client.embeddings.create(input=[chunk], model=embed_model).data[0].embedding
    ChatBotEmbedding.objects.create(
        uuid=uuid.uuid4(),
        collection_id=chatbot_collection_uuid,
        embedding=embedding,
        document=chunk
    )
