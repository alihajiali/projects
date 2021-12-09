from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from account.models import Weblog
from blog.models import Category, Post
from .forms import login_form, register_form, create_weblog_form, edit_weblog_form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید', 'success')
                return redirect("account:account_view")
    else:
        form = login_form()
    messages.info(request, 'لطفا اطلاعات خود را وارد نمایید', 'info')
    return render(request, 'account/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = register_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # if cd['username'] is None:
            print('%'*80,cd)
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            login(request, user)
            messages.success(request, 'ثبت نام شما موفقیت آمیز بود', 'success')
            return redirect("account:account_view")
    else:
        form = register_form()
    messages.info(request, 'لطفا اطلاعات خود را وارد نمایید', 'info')
    return render(request, 'account/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت از حساب خود خارج شدید', 'success')
    return redirect("blog:post_list")


def account_view(request):
    if request.user.is_authenticated:
        weblogs = Weblog.objects.filter(owner=request.user)
        messages.info(request, 'میتوانید وبلاگ جدید بسازید یا به لیستی از وبلاگ های خود دسترسی داشته باشید', 'info')
        return render(request, 'account/account.html', {'weblogs': weblogs})
    else :
        messages.info(request, 'برای دسترسی به اطلاعات حساب خود لطفا وارد شوید', 'info')
        return redirect("account:login")


def create_weblog_view(request):
    if request.method == 'POST':
        form = create_weblog_form(request.POST, request.FILES)
        if form.is_valid():
            weblog = form.save(commit=False)
            weblog.owner = request.user
            weblog.save()
            form.save_m2m()
            messages.success(request, 'وبلاگ شما با موفقیت ساخته شد', 'success')
            return redirect(reverse('account:account_view'))
    else:
        form = create_weblog_form()
    weblogs = Weblog.objects.filter(owner=request.user)
    messages.info(request, 'لطفا اطلاعات خود را وارد نمایید', 'info')
    return render(request, 'account/create_weblog.html', {'form': form, 'weblogs': weblogs})


def weblog_content(request, username):
    this_blog = get_object_or_404(Weblog, username=username)
    posts = Post.objects.filter(weblog=this_blog)
    categorys = Category.objects.filter(owner=this_blog)
    if request.user == this_blog.owner:
        messages.info(request, 'اگر مدیر وبلاگ هستید میتوانید با کلیک روی نام وبلاگ خود در فوتر این صفحه به پنل ادمین وبلاگ خود بروید', 'info')
    return render(request, "account/weblog.html", {'categorys': categorys, 'username': username, 'posts': posts, 'this_blog': this_blog})


def weblog_category_view(request, username, category_title):
    this_blog = get_object_or_404(Weblog, username=username)
    category = get_object_or_404(Category, owner=this_blog, title=category_title)#.filter(title=category_title)
    posts = Post.objects.filter(weblog=this_blog).filter(category=category)
    categorys = Category.objects.filter(owner=this_blog)
    messages.info(request, f'پست های دسته بندی{category} را در این صفحه مشاهده میکنید', 'info')
    return render(request, "account/weblog.html", {'categorys': categorys, 'username': username, 'posts': posts, 'this_blog': this_blog})



def edit_weblog_view(request, username):
    weblog = get_object_or_404(Weblog, username=username)
    if request.user == weblog.owner:
        if request.method == 'POST':
            form = edit_weblog_form(request.POST, request.FILES, instance=weblog)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.owner = request.user
                blog.save()
                form.save_m2m()
                messages.success(request, 'وبلاگ شما با موفقیت بروز شد', 'success')
                return redirect(reverse('account:account_view'))
        else :
            form = edit_weblog_form(instance=weblog)
        weblogs = Weblog.objects.filter(owner=request.user)
        messages.info(request, 'لطفا اطلاعات خود را وارد نمایید', 'info')
        return render(request,'account/edit_weblog.html', {'form': form, 'weblogs': weblogs})
    else :
        messages.info(request, 'برای بروز رسانی وبلاگ خود باید ابتدا وارد شوید', 'info')
        return redirect("account:login")


def delete_weblog_view(request, username):
    weblog = get_object_or_404(Weblog, username=username)
    if request.user == weblog.owner:
        weblog.delete()
        messages.success(request, 'وبلاگ شما با موفقیت حذف شد', 'success')
        return redirect('account:account_view')
    else :
        messages.info(request, 'برای حذف وبلاگ خود باید ابتدا وارد شوید', 'info')
        return redirect("account:login")