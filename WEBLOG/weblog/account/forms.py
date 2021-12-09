from django import forms
from django.db.models import fields
from django.db.models.fields.related import ForeignKey
from django.forms.widgets import PasswordInput, TextInput, Textarea
from .models import Weblog
from django.contrib.auth.models import User


class login_form(forms.Form):
    username = forms.CharField(
        label='نام کاربری ', max_length=30, widget=TextInput(
            attrs={"style": "width: 80%;"}))
    password = forms.CharField(
        label='رمز عبور ', max_length=30, widget=PasswordInput(
            attrs={"style": "width: 80%;"}
        ))


class register_form(forms.Form):
    username = forms.CharField(
        label='نام کاربری ', max_length=30, widget=TextInput(
            attrs={"style": "width: 80%;"}))
    email = forms.EmailField(
        label='ایمیل ', widget=TextInput(
            attrs={"style": "width: 80%; margin-left: 27px;"}))
    password = forms.CharField(
        label='رمز عبور ', max_length=30, widget=PasswordInput(
            attrs={"style": "width: 80%"}
        ))


class create_weblog_form(forms.ModelForm):
    class Meta : 
        model = Weblog
        exclude = ['owner']

        widgets ={
            'username': TextInput(attrs={"style": "width: 80%;margin-left: 10%;"}),
            'title': TextInput(attrs={"style": "width: 80%;margin-left: 12%;"}),
            'biography': Textarea(attrs={"style": "width: 80%;margin-left: 13%;"}),
        }
        

class edit_weblog_form(forms.ModelForm):
    class Meta : 
        model = Weblog
        exclude = ['owner', 'category']

        widgets ={
            'username': TextInput(attrs={"style": "width: 80%;margin-left: 10%;"}),
            'title': TextInput(attrs={"style": "width: 80%;margin-left: 12%;"}),
            'biography': Textarea(attrs={"style": "width: 80%;margin-left: 13%;"}),
        }