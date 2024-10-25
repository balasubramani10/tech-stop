from django.contrib import admin
from django.urls import path, include
from django.conf import settings # type: ignore
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('management/', include("management.urls"))
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
