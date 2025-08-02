from django.urls import path
from . import views


urlpatterns = [
    path('view-all-reports/', views.viewAllReports, name='view_all_reports'),
    path('submit-report/', views.submitReport, name='submit_report'),
    path('view-pending-report/', views.viewPendingReports, name='view_pending_report'),
]