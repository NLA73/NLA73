from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    
    # TAMBAHKAN BARIS INI:
    path('simpan-resume/', views.simpan_resume_view, name='simpan_resume'),
]