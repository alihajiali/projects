from django.contrib import admin
from .models import Post, Comment, Category, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'publish_on', 'status')
    list_filter = ('status', 'writer', 'publish_on')
    list_editable = ('status',)
    search_fields = ('title', 'body')
    raw_id_fields = ('writer',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'title', 'desc', 'created_on')
    list_filter = ('created_on',)
    raw_id_fields = ('post',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'title')
    
admin.site.register(Tag)