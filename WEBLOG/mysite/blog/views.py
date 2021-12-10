from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment, Post, Tag, Category
from .forms import create_post_form, create_category_form, create_comment_form, create_tag_form
from account.models import Weblog
from django.urls import reverse
from django.contrib import messages
import datetime


def all_post(request):
    all_post = Post.objects.filter(status="PUBLISH").order_by('-id')
    if request.method == 'POST':
        search = request.POST['search']
        all_post = Post.objects.filter(title__contains=search)
    return render(request, "blog/all_post.html", {"posts": all_post})


def popular_post(request):
    posts = Post.objects.filter(like_count__gt=10).order_by('-id')
    messages.info(request, 'تمام پست هایی که بیشتر از ۱۰ لایک داشته اند را میتوانید در این صفحه ببینید', 'info')
    return render(request, "blog/all_post.html", {"posts": posts})


def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    count = post.like_count
    user = request.user
    if user.is_authenticated:
        if user in post.like.all():
            post.like.remove(user)
            post.like_count = count-1
            post.save()
        else :
            post.like.add(user)
            post.like_count = count+1
            post.save()
        messages.success(request, 'لایک شما روی این پست ثبت / حذف شد', 'success')
        return redirect(f'/{slug}')
    else :
        messages.warning(request, 'لطفا برای لایک کردن ابتدا وارد شوید', 'warning')
        return redirect('account:login')



def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            form = create_comment_form(request.POST, request.FILES)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post=post
                comment.owner=request.user
                comment.save()
                messages.success(request, 'نظر شما با موفقیت ثبت شد', 'success')
                return redirect(f'/{slug}')
        else :
            messages.warning(request, 'برای ثبت نظر لطفا ابتدا وارد شوید', 'warning')
            return redirect('account:login')
    elif request.user != post.writer:
        form = create_comment_form()
        messages.info(request, 'میتوانید پست ها را لایک یا کامنت بگذارید', 'info')
        return render(request, "blog/post_detail.html", {'post': post, 'comments': comments, 'form': form})
    else :
        form = create_comment_form()
        messages.info(request, 'شما به عنوان ناشر پست وارد شده اید پس میتوانید پست خود را ویرایش یا حذف کنید', 'info')
        return render(request, "blog/post_detail_admin.html", {'post': post, 'comments': comments, 'form': form})



def add_post_view(request, username):
    this_blog = get_object_or_404(Weblog, username=username)
    if request.user == this_blog.owner:
        if request.method == 'POST':
            form = create_post_form(this_blog, request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.like_count = 0
                post.writer = this_blog.owner
                post.weblog = this_blog
                post.save()
                form.save_m2m()
                messages.success(request, 'پست شما با موفقیت منتشر شد', 'success')
                return redirect(f"/{username}/admin")
        else:
            messages.info(request, 'لطفا اطلاعات خواسته شده را وارد نمایید', 'info')
            form = create_post_form(this_blog)
            return render(request, 'blog/weblog_panel.html', {'form': form, 'this_blog': this_blog})
    else:
        messages.warning(request, 'برای انتشار پست لطفا ابتدا وارد شوید', 'warning')
        return redirect("account:login")


def edit_post(request, slug):
    post_ = get_object_or_404(Post, slug=slug)
    this_blog = post_.weblog
    if request.user == this_blog.owner:
        if request.method == 'POST':
            form = create_post_form(this_blog, request.POST, request.FILES, instance=post_)
            if form.is_valid():
                post = form.save(commit=False)
                post.like_count = post_.like_count
                post.writer = this_blog.owner
                post.weblog = this_blog
                post.save()
                form.save_m2m()
                messages.success(request, 'پست شما با موفقیت ویرایش شد', 'success')
                return redirect(f"/{slug}")
        else :
            messages.info(request, 'لطفا اطلاعات مورد نظر خود را تغییر دهید', 'info')
            form = create_post_form(this_blog, instance=post_)
        return render(request, 'blog/weblog_panel.html', {'form': form,  'this_blog': this_blog})
    else:
        messages.warning(request, 'برای ویرایش پست های خود لطفا ابتدا وارد شوید', 'warning')
        return redirect("account:login")


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.writer:
        post.delete()
        messages.success(request, 'پست شما با موفقیت حذف گردید', 'success')
        return redirect('/')
    else:
        messages.warning(request, 'برای حذف پست های خود لطفا ابتدا وارد شوید', 'warning')
        return redirect("account:login")



def add_category_view(request, username):
    weblogs = Weblog.objects.filter(owner=request.user)
    this_blog = get_object_or_404(Weblog, username=username)
    categorys = Category.objects.filter(owner=this_blog)
    if request.user == this_blog.owner:
        if request.method == 'POST':
            form = create_category_form(this_blog, request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.owner = this_blog
                category.save()
                messages.success(request, 'دسته بندی شما با موفقیت ساخته شد', 'success')
                return redirect(f"/{username}/admin/category")
        else:
            form = create_category_form(this_blog)
            messages.info(request, 'لطفا اطلاعات خواسته شده را وارد نمایید', 'info')
        return render(request, 'blog/manage_category.html', {'form': form, 'weblogs': weblogs, 'this_blog': this_blog, 'categorys': categorys})
    else:
        messages.warning(request, 'برای ایجاد دسته بندی ابتدا وارد شوید', 'warning')
        return redirect("account:login")



def edit_category_view(request, username, category_title):
    weblogs = Weblog.objects.filter(owner=request.user)
    this_blog = get_object_or_404(Weblog, username=username)
    categorys = Category.objects.filter(owner=this_blog)
    category_ = get_object_or_404(Category, title=category_title)
    if request.user == this_blog.owner:
        if request.method == 'POST':
            form = create_category_form(this_blog, request.POST, instance=category_)
            print("%"*100)
            print(form)
            if form.is_valid():
                print("%"*100)
                category = form.save(commit=False)
                category.owner = this_blog
                messages.success(request, 'دسته بندی شما با موفقیت ویرایش شد', 'success')
                category.save()
                return redirect(f"/{username}/admin/category")
        else:
            form = create_category_form(this_blog, instance=category_)
            messages.info(request, 'لطفا اطلاعات مورد نظر خود را تغییر دهید', 'info')
        return render(request, 'blog/manage_category.html', {'form': form, 'weblogs': weblogs, 'this_blog': this_blog, 'categorys': categorys})
    else:
        messages.warning(request, 'برای ویرایش دسته بندی های خود ابتدا وارد شوید', 'warning')
        return redirect("account:login")


def delete_category_view(request, username, category_title):
    category = get_object_or_404(Category, title=category_title)
    if request.user == category.owner.owner:
        category.delete()
        messages.success(request, 'دسته بندی شما با موفقیت حذف گردید', 'success')
        return redirect(f"/{username}/admin/category")
    else:
        messages.warning(request, 'برای حذف دسته بندی های خود ابتدا وارد شوید', 'warning')
        return redirect("account:login")



def add_tag_view(request, username):
    weblogs = Weblog.objects.filter(owner=request.user)
    this_blog = get_object_or_404(Weblog, username=username)
    tags = Tag.objects.filter(owner=this_blog)
    if request.user == this_blog.owner:
        if request.method == 'POST':
            form = create_tag_form(request.POST)
            if form.is_valid():
                tag = form.save(commit=False)
                tag.owner = this_blog
                tag.save()
                messages.success(request, 'تگ شما با موفقیت ثبت گردید', 'success')
                return redirect(f"/{username}/admin/tag")
        else:
            form = create_tag_form()
            messages.info(request, 'لطفا اطلاعات خواسته شده را وارد نمایید', 'info')
        return render(request, 'blog/manage_tag.html', {'form': form, 'weblogs': weblogs, 'this_blog': this_blog, 'tags': tags})
    else:
        messages.warning(request, 'برای ایجاد تگ جدید لطفا ابتدا وارد شوید', 'warning')
        return redirect("account:login")



def edit_tag_view(request, username, tag_title):
    weblogs = Weblog.objects.filter(owner=request.user)
    this_blog = get_object_or_404(Weblog, username=username)
    tags = Tag.objects.filter(owner=this_blog)
    tag_ = get_object_or_404(Tag, title=tag_title)
    if request.user == this_blog.owner:
        if request.method == 'POST':
            form = create_tag_form(request.POST, instance=tag_)
            if form.is_valid():
                tag = form.save(commit=False)
                tag.owner = this_blog
                tag.save()
                messages.success(request, 'تگ شما با موفقیت ویرایش گردید', 'success')
                return redirect(f"/{username}/admin/tag")
        else:
            form = create_tag_form(instance=tag_)
            messages.info(request, 'لطفا اطلاعات مورد نظر خود را تغییر دهید', 'info')
        return render(request, 'blog/manage_tag.html', {'form': form, 'weblogs': weblogs, 'this_blog': this_blog, 'tags': tags})
    else:
        messages.warning(request, 'برای ویرایش تگ های خود لطفا ابتدا وارد شوید', 'warning')
        return redirect("account:login")


def delete_tag_view(request, username, tag_title):
    tag = get_object_or_404(Tag, title=tag_title)
    if request.user == tag.owner.owner:
        tag.delete()
        messages.success(request, 'تگ شما با موفقیت حذف گردید', 'success')
        return redirect(f"/{username}/admin/tag")
    else:
        messages.warning(request, 'برای حذف تگ خود لطفا ابتدا وارد شوید', 'warning')
        return redirect("account:login")
