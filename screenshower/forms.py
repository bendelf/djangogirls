from django import forms
from .models import Project, Paroi, Volume, RefPiece
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('title', 'text')


class ParoiForm(forms.ModelForm):

    class Meta:
        model = Paroi
        fields = ('name', 'l_finie', 'h_finie')


class VolumeForm(forms.ModelForm):
    """ Class for only see volume fixe """

    class Meta:
        model = Volume
        fields = ('name', 'type', 'glass', 'l_cste')


class PieceForm(forms.ModelForm):
    """ Class for only see volume fixe """
    class Meta:
        model = RefPiece
        fields = '__all__'


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'password',
            'id': 'password'
        }
))
