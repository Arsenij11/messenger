from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='username', related_name='account')
    name = models.CharField(max_length=100,  verbose_name='имя')
    registration_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата Регистрации')
    profile_picture = models.ImageField(upload_to='photo/players/%Y/%m/%d',
                                        default='photo/players/default/Аватарка по умолчанию.jpg',
                                        verbose_name='Фото профиля')

    about = models.TextField(blank=True, null=True, verbose_name='Описание')
    sex = models.CharField(max_length = 6 ,choices = list(map(lambda x: (x[0], x[1],),[('Male', 'Мужской',), ('Female', 'Женский')])), verbose_name='Пол')
    username = models.SlugField(max_length=150)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main page', kwargs = {'username' : self.username})

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class Chat(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, default=None, related_name='chatadmin')
    is_private = models.ForeignKey('PrivateChat', null=True, default=None, on_delete=models.CASCADE,
                                   verbose_name='Приватный чат', related_name='chatseconduser')
    about = models.TextField(blank=True, null=True)
    chat_photo = models.ImageField(upload_to='photo/chat/%Y/%m/%d',
                                    default='photo/chat/default/Аватарка чата по умолчанию.jpg',
                                    verbose_name='Фото чата', null=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chat', kwargs = {'chat_id' : self.pk})

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['id']


class PrivateChat(models.Model):
    second_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='privatechatseconduser')

    def __str__(self):
        return str(self.second_user)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='message')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='messagefromuser')
    message = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} написал в чате {self.chat} сообщение "{self.message}"'

    def preview(self):
        return self.message[:10] + '...'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['send_time']

class Participants(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='users', null=True)

    def __str__(self):
        return f'Пользователь {self.user} был добавлен в чат {self.chat}'