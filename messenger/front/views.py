from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from rest_framework.authtoken.models import Token

from chats.models import Account, Chat, Message, Participants
from .forms import CreateProfile


# Create your views here.



class Main(LoginRequiredMixin, generic.DetailView):
    model = Account
    template_name = 'main.html'
    slug_url_kwarg = 'username'
    context_object_name = 'account'

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        obj = get_object_or_404(Account, username=username)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Account.objects.filter(user_id = request.user.id).exists():
            return redirect(reverse('create_profile'))
        elif not Account.objects.filter(user_id = request.user.id, username = self.kwargs['username']).exists():
            return redirect(reverse('main page', kwargs={'username' : self.kwargs['username']}))

        return super(Main, self).dispatch(request, *args, **kwargs)


class ProfileCreate(LoginRequiredMixin,generic.CreateView):
    form_class = CreateProfile
    template_name = 'create_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'создание профиля'
        return context

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        f.username = self.request.username
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if Account.objects.filter(user_id = request.user.id).exists():
            return redirect(reverse('main page', kwargs={'username' : Account.objects.get(user_id = request.user.id).username}))

        return super(ProfileCreate, self).dispatch(request, *args, **kwargs)


class ProfileUpdate(LoginRequiredMixin, generic.CreateView):
    model = Account
    template_name = 'create_profile.html'
    fields = ['name', 'about', 'profile_picture', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'обновление профиля'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Account.objects.filter(user_id=request.user.id).exists():
            return redirect(reverse('create_profile'))
        elif not Account.objects.filter(user_id=request.user.id, username=self.kwargs['username']).exists():
            return redirect(reverse('main page', kwargs={'username': self.kwargs['username']}))

        return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)

class AllChats(LoginRequiredMixin, generic.ListView):
    model = Chat
    template_name = 'chats.html'
    context_object_name = 'chats'


    def get_queryset(self):
        return Chat.objects.filter(admin=Account.objects.get(user_id=self.request.user.id))

    def dispatch(self, request, *args, **kwargs):
        if not Account.objects.filter(user_id=request.user.id).exists():
            return redirect(reverse('create_profile'))

        return super(AllChats, self).dispatch(request,*args, **kwargs)



class GroupPrivateChat(LoginRequiredMixin, generic.DetailView):
    template_name = 'chat.html'
    context_object_name = 'ourchat'
    pk_url_kwarg = 'chat_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = []
        participants = Participants.objects.filter(user_id = Account.objects.get(user_id = self.request.user.id).id)
        for p in participants:
            context['chats'].append(Chat.objects.get(pk=p.chat_id))

        admin = Chat.objects.filter(admin=Account.objects.get(user_id = self.request.user.id).id)
        for a in admin:
            if a not in context['chats']:
                context['chats'].append(a)

        context['token'] = Token.objects.get(user_id = self.request.user.id).key

        return context

    def get_object(self, queryset=None):
        chat_id = self.kwargs['chat_id']
        return Chat.objects.get(pk=chat_id)

    def dispatch(self, request, *args, **kwargs):
        if not Account.objects.filter(user_id=request.user.id).exists():
            return redirect(reverse('create_profile'))
        elif not Chat.objects.filter(admin=request.user.id, pk=self.kwargs['chat_id']).exists():
            return redirect(reverse('chats'))



        return super(GroupPrivateChat, self).dispatch(request, *args, **kwargs)





