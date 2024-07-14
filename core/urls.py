from django.urls import path
from .views import ChatBotListCreateView, ChatBotDetailView

urlpatterns = [
    path('', ChatBotListCreateView.as_view(), name='chatbot-list-create'),
    path('<uuid:uuid>/', ChatBotDetailView.as_view(), name='chatbot-detail'),
]