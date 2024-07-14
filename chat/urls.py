from django.urls import path
from .views import ChatDetailView, ChatListCreateView

urlpatterns = [
    path('', ChatListCreateView.as_view(), name='chat-list'),
    path('<uuid:uuid>', ChatDetailView.as_view(), name='chat-details'),
]