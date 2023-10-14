from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('',views.index, name='index'),
    path('settings',views.settings, name="settings"),
    path('settings/deletion',views.delete_user_view, name='delete_account'),
   ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)