from django import forms
from django.contrib.auth import authenticate, login, logout
from projects.models import Veroeffentlichung, Ort


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Benutzername und/oder Passwort ist falsch.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class VeroeffentlichungForm(forms.ModelForm):

    class Meta:
        model = Veroeffentlichung


class OrtForm(forms.ModelForm):

    class Meta:
        model = Ort
        exclude = ('polygon','polygontype')
        
        