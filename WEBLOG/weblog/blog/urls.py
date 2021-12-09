from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.all_post, name='post_list'),
    path('<username>/admin/', views.add_post_view, name='add_post'),
    path('edit/<slug>', views.edit_post, name='edit_post'),
    path('delete/<slug>', views.delete_post, name='delete_post'),
    path('<slug:slug>', views.post_detail, name="post_detail"),
    path('popular_post/', views.popular_post, name="popular_post"),
    path('<slug:slug>/like', views.post_like, name="post_like"),

    path('<username>/admin/category/', views.add_category_view, name='add_category'),
    path('<username>/admin/category/edit/<category_title>', views.edit_category_view, name='edit_category'),
    path('<username>/admin/category/delete/<category_title>', views.delete_category_view, name='delete_category'),
    
    path('<username>/admin/tag/', views.add_tag_view, name='add_tag'),
    path('<username>/admin/tag/edit/<tag_title>', views.edit_tag_view, name='edit_tag'),
    path('<username>/admin/tag/delete/<tag_title>', views.delete_tag_view, name='delete_tag'),
]