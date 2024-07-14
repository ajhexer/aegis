from .models import Conversation, Message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import uuid as UUID
from core.models import ChatBot
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q


class ChatDetailView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'chat-details.html'

    def get(self, request, uuid):
        # Get the conversation and its messages
        conversation = Conversation.objects.get(pk=uuid)
        messages = conversation.messages.all()
        if conversation.title == "" and len(messages)>0:
            conversation.title = messages[0].user_input
            conversation.save()
        if len(messages) == 0:
            context = {'messages': [], "last_message": []}
        elif len(messages) == 1:
            context = {'messages': [], "last_message": [messages[0]]}
        else:
            context = {'messages': messages[:len(messages)-1], "last_message": [messages[len(messages)-1]]}
        context["conversation_id"] = conversation.uuid
        # context = {'conversation': conversation}
        return render(request, self.template_name, context)

    def post(self, request, uuid):
        # Handle form submission (sending a new message)
        user_input = request.POST.get('input')
        conversation = Conversation.objects.get(pk=uuid)
        chatbot = conversation.chatbot
        model_answer = chatbot.generate_answer(user_input)
        message = Message.objects.create(conversation=conversation, user_input=user_input, model_answer=model_answer.strip())
        conversation.timestamp = message.timestamp
        conversation.save()
        return redirect('chat-details', uuid=uuid)

    def put(self, request, uuid):
        conversation = Conversation.objects.get(pk=uuid)
        chatbot = conversation.chatbot
        last_message = conversation.messages.last()
        last_message.model_answer = chatbot.generate_answer(last_message.user_input)
        last_message.save()
        return redirect('chat-details', uuid=uuid)

class ChatListCreateView(LoginRequiredMixin, View):
    template_name = 'chat-list.html'
    login_url = 'login'
    paginate_by = 5

    def get(self, request):
        user_chats = Conversation.objects.filter(user=request.user)
        user_chatbots = ChatBot.objects.filter(user=request.user)
        page = request.GET.get('page', 1)
        paginator = Paginator(user_chats, self.paginate_by)

        try:
            user_chats = paginator.page(page)
        except PageNotAnInteger:
            user_chats = paginator.page(1)
        except EmptyPage:
            user_chats = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'user_chats': user_chats, 'user_chatbots': user_chatbots})

    def post(self, request):
        chatbot = ChatBot.objects.get(pk=request.POST.get('chatbot'))
        conversation = Conversation.objects.create(chatbot=chatbot, user=request.user, uuid=UUID.uuid4())
        return redirect('chat-details', uuid=conversation.uuid)

class SearchView(LoginRequiredMixin, ListView):
    login_url = 'account_login'
    model = Conversation
    context_object_name = 'user_chats'
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return (Conversation.objects.filter(
                Q(title__icontains=query) | Q(messages__user_input__icontains=query) | Q(
                    messages__model_answer__icontains=query))).distinct()
        else:
            return None


