from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Weblog(models.Model):
    Religious = 'RE'
    politicalـandـsocial = 'PS'
    CultureـandـArt = 'CA'
    sportـandـentertainment = 'SE'
    Educationalـandـscientific = 'ES'
    lifeـstyle = 'LS'
    Economical = 'EC'
    medical = 'ME'
    Personal = 'PE'
    CATEGORY = (
        ('Religious', 'مذهبی'),
        ('politicalـandـsocial', 'سیاسی و اجتماعی'),
        ('CultureـandـArt', 'فرهنگ و هنر'),
        ('sportـandـentertainment', 'ورزش و سرگرمی'),
        ('Educationalـandـscientific', 'آموزشی و علمی'),
        ('lifeـstyle', 'سبک زندگی'),
        ('Economical', 'اقتصادی'),
        ('medical', 'پزشکی'),
        ('Personal', 'شخصی')
    )
    username = models.CharField(max_length=100, verbose_name='نام کاربری')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    image = models.ImageField(verbose_name='تصویر', null= True, blank=True)
    owner = models.ForeignKey(User, on_delete=CASCADE, verbose_name='نویسنده', null=True, blank=True)
    category = models.CharField(max_length=26, choices=CATEGORY, default=Personal, verbose_name='نوع')
    biography = models.TextField(verbose_name='شرح')

    def __str__(self) -> str:
        return self.username