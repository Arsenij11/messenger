from django import forms

from API.models import Account


class CreateProfile(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'profile_picture', 'about', 'sex',]

