from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login, name='login'),
    # path('registration/', views.registration, name='registration'),
    path('register/', views.register, name='register'),
    path('login/', views.loginCheck, name='login'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile-edit/', views.profile_edit, name='profile_edit'),
    path('logout/', views.logout_view, name='logout'),
    path('view-my-posts/', views.viewMyPosts, name='view_my_posts'),
    path('view-my-reports/', views.viewMyReports, name='view_my_reports'),
    path('super-admin-dashboard/', views.superAdminDashboard, name='super_admin_dashboard'),
]