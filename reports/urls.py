from django.urls import path
from . import views


urlpatterns = [
    path('view-all-reports/', views.viewAllReports, name='view_all_reports'),
    path('submit-report/', views.submitReport, name='submit_report'),
    path('view-pending-report/', views.viewPendingReports, name='view_pending_report'),
    path('edit-report/<int:report_id>/', views.editReport, name='edit_report'),
    path('approve-report/<int:report_id>/', views.approveReport, name='approve_report'),
    path('delete-report/<int:report_id>/', views.deleteReport, name='delete_report'),
    path('report-status-update/<int:report_id>/', views.reportStatusUpdateView, name='report_status_update'),
    path('report-status-update-pending/<int:report_id>/', views.reportStatusUpdatePending, name='report_status_update_pending'),
]