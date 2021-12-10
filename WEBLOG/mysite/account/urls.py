from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path("register/", views.register_view, name='register'),
    path("logout/", views.logout_view, name='logout'),
    path("account/", views.account_view, name='account_view'),

    path("create_weblog/", views.create_weblog_view, name='create_weblog_view'),
    path("<username>/", views.weblog_content, name="weblog_content"),
    # path("<username>/<category_title>/", views.weblog_category_view, name="weblog_category"),

    path("account/edit-weblog-<username>/", views.edit_weblog_view, name="edit_weblog"),
    path("account/delete-weblog-<username>/", views.delete_weblog_view, name="delete_weblog"),
]