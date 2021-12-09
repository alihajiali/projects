from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("blog.urls", namespace="blog")),
    path('account/', include("account.urls", namespace="account")),

    # path("<username>/", views.weblog_content, name="weblog_content"),
    path("<username>/<category_title>/", views.weblog_category_view, name="weblog_category"),

    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)