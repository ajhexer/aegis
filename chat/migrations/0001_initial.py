# Generated by Django 4.2.7 on 2023-12-01 16:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_alter_chatbotembedding_collection'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('title', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2023, 12, 1, 16, 27, 18, 660943, tzinfo=datetime.timezone.utc))),
                ('uuid', models.UUIDField(default=uuid.UUID('ea77072d-f6ed-40e1-8b7f-3c62f2b9a704'), primary_key=True, serialize=False)),
                ('chatbot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='core.chatbot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_input', models.TextField()),
                ('model_answer', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.conversation')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
