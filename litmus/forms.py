from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

""" SignUpForm uses "User" class and also adds extra fields mentioned below """

from . models import Profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,help_text='Last Name' ,required=True)
    last_name = forms.CharField(max_length=100,help_text='Last Name',required=True)
    e_mail = forms.EmailField(max_length=150,help_text='Email',required=True)
    nick_name = forms.CharField(max_length=100,help_text='Nick Name',required=True)


    class Meta:
        model = User
        fields = ('nick_name','first_name','last_name','e_mail','password1','password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['nick_name'].widget.attrs['placeholder'] = 'User Name'
        self.fields['nick_name'].widget.attrs['class'] = 'input-field'

        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['first_name'].widget.attrs['class'] = 'input-field'

        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['last_name'].widget.attrs['class'] = 'input-field'

        self.fields['e_mail'].widget.attrs['placeholder'] = 'Email ID'
        self.fields['e_mail'].widget.attrs['class'] = 'input-field'

        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password1'].widget.attrs['class'] = 'input-field'

        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['class'] = 'input-field'
