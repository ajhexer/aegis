from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import ChatBot, ChatBotCollection
import uuid as UUID
from .tasks import data_extract


class ChatBotListCreateView(View):
    template_name = 'chatbot-list.html'
    paginate_by = 5
    def get(self, request):

        user_chatbots = ChatBot.objects.filter(user=request.user)
        page = request.GET.get('page', 1)
        paginator = Paginator(user_chatbots, self.paginate_by)

        try:
            chatbots = paginator.page(page)
        except PageNotAnInteger:
            chatbots = paginator.page(1)
        except EmptyPage:
            chatbots = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'chatbots': chatbots})
    def post(self, request):
        name = request.POST.get('name')
        chatbot = ChatBot(name=name, user=request.user, uuid=UUID.uuid4())
        chatbot.save()
        return redirect('chatbot-list-create')

class ChatBotDetailView(View):
    template_name = 'chatbot-detail.html'

    def get(self, request, uuid):
        chatbot = get_object_or_404(ChatBot, uuid=uuid)
        collections = ChatBotCollection.objects.filter(chatbot=chatbot)

        return render(request, self.template_name, {'chatbot': chatbot, 'collections': collections})

    @method_decorator(csrf_exempt)
    def post(self, request, uuid):
        chatbot = get_object_or_404(ChatBot, uuid=uuid)
        name = request.POST.get('name')
        document = request.FILES.get('document')
        data_extract(document, name, uuid)

        return redirect('chatbot-detail', uuid=uuid)
