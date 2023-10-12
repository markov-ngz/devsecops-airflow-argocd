from django.urls import path
from . import views 


app_name = 'core'

urlpatterns = [
    path('',views.index, name='index'),
    path('settings',views.settings, name="settings"),
    path('settings/deletion',views.delete_user_view, name='delete_account'),
   ]