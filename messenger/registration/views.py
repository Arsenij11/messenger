import json
import random

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import requests
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView
from djoser.urls import authtoken

from .forms import LoginUserForm, RegistrationForm, UserPasswordChangeForm, Confirm_Email

from .models import EmailConfirm

# Create your views here.




class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    extra_context = {'title' : 'Авторизация'}
    password = None

    def form_valid(self, form):
        f = form.cleaned_data
        self.password = f['password']
        if EmailConfirm.objects.filter(user__username=f['username']).exists():
            return redirect(reverse('registration:confirm_email',
                                    kwargs={'username': f['username']}))
        return super().form_valid(form)

    def get_success_url(self):
        if not Token.objects.filter(user_id = self.request.user.id).exists():
            requests.post(url = 'http://127.0.0.1:8000/auth/token/login/',  data = {
                                                                            'username' : self.request.user.username,
                                                                            'password' : self.password,
                                                                            }
                          )
        return reverse_lazy('create_profile')

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect(reverse('main page', kwargs={'username': request.user.username}))
    #
    #     return super(LoginView, self).dispatch(request, *args, **kwargs)

class Registration(CreateView):
    template_name = 'register.html'
    form_class = RegistrationForm
    extra_context = {'title': 'Регистрация'}
    username = None


    def form_valid(self, form):
        form = form.save(commit=False)
        self.username = form.username
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('registration:confirm_email', kwargs={'username': self.username})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('main page', kwargs={'username' : request.user.username}))
        # if User.objects.filter(pk = request.user.id).exists():
        #     if EmailConfirm.objects.filter(user_id = request.user.id).exists():
        #         return redirect(reverse('registration:confirm_email', kwargs={'username' : request.user.username}))
        #     else:
        #         return redirect('registration:login')

        return super(Registration, self).dispatch(request, *args, **kwargs)




class UserPasswordChange(PasswordChangeView):
    template_name = 'password_change_form.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('registration:password_change_done')



def confirm_email(request, username):
    user_id = get_object_or_404(User, username = username).id
    if not EmailConfirm.objects.filter(user_id = user_id).exists():
        return redirect(reverse('registration:login'))
    # if request.user.id != user_id:
    #     return redirect(reverse('registration:login'))
    if request.method == 'POST':
        form = Confirm_Email(request.POST,user_id=user_id)
        if form.is_valid():
            check_key = EmailConfirm.objects.filter(key=form.cleaned_data['key'], user_id=user_id)
            check_key.delete()
            return render(request, 'successful_registration.html')


    else:
        form = Confirm_Email()

    return render(request, 'confirm_email.html', {'form' : form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect(reverse('registration:login'))