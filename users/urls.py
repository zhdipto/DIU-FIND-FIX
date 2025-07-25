from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login, name='login'),
    # path('registration/', views.registration, name='registration'),
    path('register/', views.register, name='register'),
    path('loginCheck/', views.loginCheck, name='loginCheck'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
]