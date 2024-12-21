from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='username')
    name = models.CharField(max_length=100,  verbose_name='имя')
    registration_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата Регистрации')
    profile_picture = models.ImageField(upload_to='photo/players/%Y/%m/%d',
                                        default='photo/players/default/Аватарка по умолчанию.jpg',
                                        verbose_name='Фото профиля')

    about = models.TextField(blank=True, null=True, verbose_name='Описание')
    online = models.BooleanField(default=False)
    sex = models.CharField(max_length = 6 ,choices = list(map(lambda x: (x[0], x[1],),[('Male', 'Мужской',), ('Female', 'Женский')])), verbose_name='Пол')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class Chat(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, default=None)
    is_private = models.BooleanField()
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    message = models.TextField()

    def __str__(self):
        return f'{self.user} in chat {self.chat} : {self.message}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
