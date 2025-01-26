import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from djoser.conf import User
from rest_framework.authtoken.models import Token

from API.models import Account, Chat, Message, Participants, PrivateChat
from .forms import CreateProfile
# from ..API.models import Account, Chat, Message, Participants, PrivateChat

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
        f.username = self.request.user.username
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if Account.objects.filter(user_id = request.user.id).exists():
            return redirect(reverse('main page', kwargs={'username' : request.user.username}))

        return super(ProfileCreate, self).dispatch(request, *args, **kwargs)


class ProfileUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Account
    template_name = 'create_profile.html'
    fields = ['name', 'about', 'profile_picture', ]
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'обновление профиля'
        return context

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        f.username = self.request.user.username
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not Account.objects.filter(user_id=request.user.id).exists():
            return redirect(reverse('create_profile'))
        elif not Account.objects.filter(user_id=request.user.id, username=self.kwargs['username']).exists():
            return redirect(reverse('main page', kwargs={'username': self.kwargs['username']}))

        return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        obj = get_object_or_404(Account, username=username)
        return obj

class DeleteProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = 'delete_profile.html'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление аккаунта'
        context['account'] = Account.objects.get(username = self.kwargs['username'])
        return context


    def dispatch(self, request, *args, **kwargs):
        if not Account.objects.filter(username = self.kwargs['username']).exists():
            return redirect(reverse('create_profile'))
        elif Account.objects.get(username = self.kwargs['username']).user.id != request.user.id:
            return redirect(reverse('main page', kwargs = {'username' : request.user.username}))

        return super(DeleteProfile, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user_id = self.request.user.id
        requests.post('http://127.0.0.1:8000/auth/token/logout/', headers={
            'Authorization': 'Token ' + Token.objects.get(user_id=self.request.user.id).key})
        logout(self.request)
        User.objects.get(pk = user_id).delete()
        return redirect(reverse('registration:login'))






class AllChats(LoginRequiredMixin, generic.ListView):
    template_name = 'chats.html'
    context_object_name = 'chats'


    def get_queryset(self):
        chats_ids = []
        account = self.request.user.account
        for p in Participants.objects.filter(user_id=account.id):
            chats_ids.append(p.chat_id)

        if Chat.objects.filter(Q(admin_id=account.id) | Q(is_private__second_user=account)).exists():
            for c in Chat.objects.filter(Q(admin_id=account.id) | Q(is_private__second_user=account)):
                chats_ids.append(c.pk)

        return Chat.objects.filter(id__in = chats_ids)

    def dispatch(self, request, *args, **kwargs):
        if not Account.objects.filter(user_id=request.user.id).exists():
            return redirect(reverse('create_profile'))
        if (not Chat.objects.filter(Q(admin_id = request.user.account.id) |
                                   Q(is_private__second_user_id = request.user.account.id) &
                                   ~Q(is_private=None)).exists() and
                not Participants.objects.filter(user_id = request.user.account.id).exists()):
            return redirect(reverse('new_chat'))


        # Добавить Participants
        return super(AllChats, self).dispatch(request,*args, **kwargs)



class GroupPrivateChat(LoginRequiredMixin, generic.DetailView):
    template_name = 'chat.html'
    context_object_name = 'ourchat'
    pk_url_kwarg = 'chat_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = []
        chats_ids = []
        account = self.request.user.account
        for p in Participants.objects.filter(user_id=account.id):
            chats_ids.append(p.chat_id)

        if Chat.objects.filter(Q(admin_id = account.id) | Q(is_private__second_user = account)).exists():
            for c in Chat.objects.filter(Q(admin_id = account.id) | Q(is_private__second_user = account)):
                chats_ids.append(c.pk)


        context['chats'] = Chat.objects.filter(id__in=chats_ids)

        context['token'] = Token.objects.get(user_id = self.request.user.id).key

        return context

    def get_object(self, queryset=None):
        chat_id = self.kwargs['chat_id']
        return Chat.objects.get(pk=chat_id)

    def dispatch(self, request, *args, **kwargs):
        if not Account.objects.filter(user_id=request.user.id).exists():
            return redirect(reverse('create_profile'))
        if not Chat.objects.filter(pk = self.kwargs['chat_id']).exists():
            return redirect('new_chat')
        chat = Chat.objects.get(pk = self.kwargs['chat_id'])
        if not Participants.objects.filter(user_id=request.user.account.id, chat_id=self.kwargs['chat_id']).exists() \
                and chat.is_private is None:
            return redirect(reverse('chats'))
        if chat.is_private is not None:
            if chat.admin.id != request.user.account.id and chat.is_private.second_user != request.user.account:
                return redirect('new_chat')


        return super(GroupPrivateChat, self).dispatch(request, *args, **kwargs)


class CreateChat(LoginRequiredMixin, generic.CreateView):
    template_name = 'new_chat.html'
    model = Chat
    fields = ['name', 'about', 'chat_photo']

    def form_valid(self, form):
        f = form.save(commit = False)
        f.is_private = None
        f.admin = Account.objects.get(user_id = self.request.user.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание чата'
        return context

    def get_success_url(self):
        chat = list(Chat.objects.filter(admin_id = self.request.user.account.id, is_private = None))[-1]
        Participants.objects.create(user_id = chat.admin.id, chat_id = chat.id)
        return super().get_success_url()

    def dispatch(self, request, *args, **kwargs):
        if not Account.objects.filter(user_id = request.user.id).exists():
            return redirect(reverse('create_profile'))

        return super(CreateChat, self).dispatch(request, *args, **kwargs)



class UpdateChat(LoginRequiredMixin, generic.UpdateView):
    template_name = 'new_chat.html'
    model = Chat
    fields = ['name', 'about', 'chat_photo']
    pk_url_kwarg = 'chat_id'

    def form_valid(self, form):
        f = form.save(commit = False)
        f.is_private = None
        f.admin = Account.objects.get(user_id = self.request.user.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновление чата'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Chat.objects.filter(pk=self.kwargs['chat_id']).exists():
            return redirect(reverse('new_chat'))

        if Chat.objects.get(pk=self.kwargs['chat_id']).is_private is not None:
            return redirect(reverse('chat', kwargs={'chat_id': self.kwargs['chat_id']}))

        if Chat.objects.get(pk=self.kwargs['chat_id']).admin.pk != request.user.account.id:
            return redirect(reverse('chat', kwargs={'chat_id': self.kwargs['chat_id']}))

        return super(UpdateChat, self).dispatch(request, *args, **kwargs)

class DeleteChat(LoginRequiredMixin, generic.TemplateView):
    template_name = 'delete_chat.html'
    pk_url_kwarg = 'chat_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление чата'
        context['chat'] = Chat.objects.get(pk = self.kwargs['chat_id'])
        return context


    def dispatch(self, request, *args, **kwargs):
        if not Chat.objects.filter(pk = self.kwargs['chat_id']).exists():
            return redirect(reverse('new_chat'))

        if Chat.objects.get(pk = self.kwargs['chat_id']).is_private is not None:
            return redirect(reverse('chat', kwargs={'chat_id' : self.kwargs['chat_id']}))

        if Chat.objects.get(pk = self.kwargs['chat_id']).admin.pk != request.user.account.id:
            return redirect(reverse('chat', kwargs= {'chat_id' : self.kwargs['chat_id']}))

        return super(DeleteChat, self).dispatch(request, *args, **kwargs)


@login_required
def toinvite(request, user_id):
    if not Account.objects.filter(user_id=request.user.id).exists():
        return redirect(reverse('create_profile'))
    elif not Account.objects.filter(id = user_id).exists():
        return redirect(reverse('main page', kwargs = {'username' : request.user.username}))
    elif request.user.account.id == int(user_id):
        return redirect(reverse('main page', kwargs = {'username' : request.user.username}))

    chats = list(Chat.objects.filter(admin_id = request.user.account.id, is_private = None))

    if len(chats) == 0:
        return render(request, 'invalidinvite.html', context= {'title' : 'Бесед нет'})

    truechats = []
    for chat in chats:
        if not Participants.objects.filter(chat_id = chat.id, user_id = user_id).exists():
            truechats.append(chat)

    if len(truechats) == 0:
        return render(request, 'nothingtoinvite.html', context={'guest' : Account.objects.get(id = user_id).username,
                                                                'title' : 'Бесед нет'})

    return render(request, 'invite.html', context={'title' : 'Пригласить в беседу', 'chats' : truechats, 'user_id' : user_id,
                                                   'token' : Token.objects.get(user_id = request.user.id).key})


@login_required
def createprivatechat(request, username):
    if not Account.objects.filter(user_id = request.user.id).exists():
        return redirect('create_profile')
    if not Account.objects.filter(user__username=username).exists():
        return redirect(reverse('main page', kwargs={'username' : request.user.username}))

    if Chat.objects.filter(admin_id = request.user.account.id, is_private__second_user__username = username).exists() or\
        Chat.objects.filter(admin__username = request.user.username, is_private__second_user_id = request.user.account.id).exists():
        chat = Chat.objects.filter(admin_id = request.user.account.id, is_private__second_user__username = username)
        chat = chat[0] if len(chat) != 0 else Chat.objects.filter(admin__username = request.user.username,
                                                               is_private__second_user_id = request.user.account.id)[0]
        return redirect(reverse('chat', kwargs = {'chat_id' : chat.id}))

    if request.user.username == username:
        return redirect(reverse('chats'))

    second_user = PrivateChat.objects.create(second_user_id = Account.objects.get(username=username).id)

    chat = Chat.objects.create(name = Account.objects.get(username=username).name, admin = request.user.account,
                               is_private = second_user, about = None,
                               chat_photo = None)

    return redirect(reverse('chat', kwargs = {'chat_id' : chat.id}))





class MoreInfo(LoginRequiredMixin, generic.DetailView):
    pk_url_kwarg = 'chat_id'
    template_name = 'moreinfo.html'
    context_object_name = 'chat'

    def get_object(self, queryset=None):
        obj = Chat.objects.get(id = self.kwargs['chat_id'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Больше информации о чате {Chat.objects.get(id = self.kwargs["chat_id"]).name}'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Chat.objects.filter(id=self.kwargs['chat_id'], is_private = None).exists():
            return render(request, 'chatnotexists.html', context={'title' : 'Данного чата не существует'})

        return super(MoreInfo, self).dispatch(request, *args, **kwargs)


class Toshow(LoginRequiredMixin, generic.ListView):
    template_name = 'toshow.html'
    context_object_name = 'participants'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Список участников беседы "{Chat.objects.get(id = self.kwargs["chat_id"]).name}"'
        context['chat'] = Chat.objects.get(id = self.kwargs['chat_id'])
        return context

    def get_queryset(self):
        participants = [p.user_id for p in Participants.objects.filter(chat_id = self.kwargs['chat_id'])]

        return Account.objects.filter(id__in = participants)

    def dispatch(self, request, *args, **kwargs):
        if not Chat.objects.filter(id=self.kwargs['chat_id'], is_private = None).exists():
            return render(request, 'chatnotexists.html', context={'title' : 'Данного чата не существует'})

        return super(Toshow, self).dispatch(request, *args, **kwargs)

# class AllMessages(generic.DetailView):
#     template_name = 'messages.html'
#     context_object_name = 'ourchat'
#
#     def get_object(self, queryset=None):
#         obj = get_object_or_404(Chat, pk = self.kwargs['chat_id'])
#         return obj
#
#     def dispatch(self, request, *args, **kwargs):
#         if not Account.objects.filter(user_id=request.user.id).exists():
#             return redirect(reverse('create_profile'))
#         if not Chat.objects.filter(pk = self.kwargs['chat_id']).exists():
#             return redirect('new_chat')
#         chat = Chat.objects.get(pk = self.kwargs['chat_id'])
#         if not Participants.objects.filter(user_id=request.user.account.id, chat_id=self.kwargs['chat_id']).exists() \
#                 and chat.is_private is None:
#             return redirect(reverse('chats'))
#         if chat.is_private is not None:
#             if chat.admin.id != request.user.account.id and chat.is_private.second_user != request.user.account:
#                 return redirect('new_chat')
#
#
#         return super(AllMessages, self).dispatch(request, *args, **kwargs)