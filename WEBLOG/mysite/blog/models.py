from django.db import models
from randomslugfield import RandomSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from account.models import Weblog
from django.contrib.auth.models import User

class Post(models.Model):
    PUBLISH = 'PU'
    DRAFT = 'DR'
    STATUS = (
        ('PUBLISH', 'انتشار'),
        ('DRAFT', 'پیش نویس')
    )
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='عنوان')
    slug = RandomSlugField(length=12, verbose_name='آدرس')
    image = models.ImageField(verbose_name='تصویر')
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    weblog = models.ForeignKey(Weblog, on_delete=models.CASCADE, verbose_name='وبلاگ')
    description = RichTextUploadingField(verbose_name="متن", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    publish_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default=PUBLISH, verbose_name='وضعیت')
    like_count = models.IntegerField(default=0, verbose_name='لایک')
    like = models.ManyToManyField(User, related_name='blog_like', verbose_name='لایک', blank=True)
    tag = models.ManyToManyField('Tag', verbose_name='تگ', related_name='tag_owner')
    category = models.ManyToManyField('Category', verbose_name='دسته')

    def __str__(self):
        return self.slug


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True, blank=True, verbose_name='پست')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='عنوان')
    desc = RichTextUploadingField(null=True, blank=True, verbose_name='متن')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')

    def __str__(self):
        return self.title


class Category(models.Model):
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True, verbose_name='پدر')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='عنوان')
    owner = models.ForeignKey(Weblog, on_delete=models.CASCADE, related_name='category_weblog', verbose_name='مالک', null=True, blank=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='عنوان')
    owner = models.ForeignKey(Weblog, on_delete=models.CASCADE, related_name='tag_weblog', verbose_name='مالک', null=True, blank=True)

    def __str__(self):
        return self.title