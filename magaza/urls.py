from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from sepet import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.siparis_onay, name="siparis_onay")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
