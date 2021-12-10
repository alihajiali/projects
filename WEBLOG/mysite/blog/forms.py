from django import forms
from django.db.models import fields
from django.db.models.fields.related import ForeignKey
from django.forms.widgets import Select, Textarea, TextInput
from .models import Post, Category, Comment, Tag
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class create_post_form(forms.ModelForm):
    def __init__(self, this_blog, *args, **kwargs):
        super (create_post_form,self ).__init__(*args,**kwargs)
        self.fields['category'].queryset = Category.objects.filter(owner=this_blog)
        self.fields['tag'].queryset = Tag.objects.filter(owner=this_blog)
    class Meta:
        model  = Post
        fields=['title','image','description','status','category','tag']
        exclude = ['writer', 'weblog', 'like', 'like_count']
        widgets ={
            'title': TextInput(attrs={"style": "width: 80%;margin-left: 10%;"}),
        }



class create_category_form(forms.ModelForm):
    def __init__(self, this_blog, *args, **kwargs):
        super (create_category_form,self ).__init__(*args,**kwargs)
        self.fields['parent'].queryset = Category.objects.filter(owner=this_blog)
    class Meta:
        model = Category
        exclude = ['owner']



class create_comment_form(forms.ModelForm):
    title = forms.CharField(label='عنوان ', max_length=30, widget=forms.TextInput(attrs={"style": "width: 80%;"}))
    desc = RichTextUploadingField()
    class Meta:
        model = Comment
        fields = ['title', 'desc']


class create_tag_form(forms.ModelForm):
    title = forms.CharField(label='عنوان ', max_length=30, widget=forms.TextInput(attrs={"style": "width: 80%;"}))
    class Meta:
        model = Tag
        exclude = ['owner']