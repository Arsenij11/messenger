from django.shortcuts import render, get_object_or_404
from django.views import generic

from chats.models import Account
from .forms import CreateProfile


# Create your views here.





def main(request, pk):
    account = get_object_or_404(Account, pk=pk)

    return render(request,'main.html', context={'title' : 'Профиль', 'account' : account})

def profile_create(request):
    return render(request,'create_profile.html', context={'title' : 'Создание профиля',})


# class ProfileCreate(generic.CreateView):
#     model = Account
#     form_class = CreateProfile
#     template_name = 'create_profile.html'
#
#     def form_valid(self, form):
#         f = form.save(commit=False)
#         f.user = self.request.user
#         return super().form_valid(form)
#
#     def dispatch(self, request, *args, **kwargs):
#         if Account.objects.filter(user = self.request.user).exists():
#             return render(request, 'main.html', context={'title' : 'Профиль',
#                                                          'account' : Account.objects.get(user_id=self.request.user.id),
#                                                          'user' : request.user})
#
#         return super(ProfileCreate, self).dispatch(request, *args, **kwargs)
#
# class ProfileUpdate(generic.CreateView):
#     model = Account
#     form_class = CreateProfile
#     template_name = 'create_profile.html'
#     pk_url_kwarg = 'account_id'
#
#     def dispatch(self, request, *args, **kwargs):
#         if Account.objects.get(pk = self.kwargs[self.pk_url_kwarg]) != Account.objects.get(user_id=self.request.user.id):
#             return render(request, 'main.html', context={'title' : 'Профиль',
#                                                          'account' : Account.objects.get(user_id=self.request.user.id),
#                                                          'user' : request.user})
#
#         return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)