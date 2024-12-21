from django import forms

from chats.models import Account


class CreateProfile(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'profile_picture', 'about', 'sex']