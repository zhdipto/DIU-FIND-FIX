from pyexpat.errors import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from reports.models import Report
from users.models import User

# Create your views here.
@login_required(login_url='login')
def viewAllReports(request):
    report = Report.objects.filter(
            is_visible=True
        ).order_by('-submitted_at')
    context = {
        "classActiveReports": "active",
        "classActiveViewAllReports": "active",
        "reports": report,
    }
    return render(request, 'viewReport/viewAllReport.html', context)

@login_required(login_url='login')
def submitReport(request):
    user = request.user
    if request.method == 'POST':
        catagory = request.POST.get('issueCategory')
        description = request.POST.get('description')
        location = request.POST.get('location')
        event_date = request.POST.get('issueDate')
        event_time = request.POST.get('issueTime')
        photo = request.FILES.get('photo')
        username = request.POST.get('username')

        if user.role == 2:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return redirect('create_post')

        report = Report.objects.create(
            user=user,
            category=catagory,
            description=description,
            location=location,
            event_date=event_date,
            event_time=event_time,
            photo=photo,
            is_visible=False,  # Default: pending admin approval
            submitted_at=timezone.now()
        )
        report.save()

        return redirect('submit_report')
    
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    context = {
        "classActiveReports": "active",
        "classActiveSubmitReport": "active",
        "user": user,
    }
    return render(request, 'submitReport/createReport.html', context)

@login_required(login_url='login')
def viewPendingReports(request):
    user = request.user
    if user.role != 2:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')
    
    report = Report.objects.filter(is_visible=False).order_by('-submitted_at')
    context = {
        "classActiveReports": "active",
        "classActiveViewPendingReports": "active",
        "reports": report,
    }
    return render(request, 'pendingReport/viewPendingReport.html', context)

@login_required(login_url='login')
def editReport(request, report_id):
    user = request.user
    if user.role != 2:
        messages.error(request, "You do not have permission to edit this report.")
        return redirect('home')
    
    report = Report.objects.get(id=report_id)
    if request.method == 'POST':
        report.category = request.POST.get('issueCategory')
        report.description = request.POST.get('description')
        report.location = request.POST.get('location')
        report.event_date = request.POST.get('issueDate')
        report.event_time = request.POST.get('issueTime')
        
        if 'photo' in request.FILES:
            report.photo = request.FILES['photo']
        
        report.last_updated_by = user
        report.save()
        return redirect('edit_report', report_id=report.id)

    context = {
        "classActiveReports": "active",
        "report": report,
    }
    return render(request, 'submitReport/editReport.html', context)

@login_required(login_url='login')
def deleteReport(request, report_id):
    user = request.user
    if user.role != 2:
        messages.error(request, "You do not have permission to delete this report.")
        return redirect('home')

    report = get_object_or_404(Report, id=report_id)
    report.delete()
    # messages.success(request, "Report deleted successfully.")
    return redirect('view_pending_report')

@login_required(login_url='login')
def approveReport(request, report_id):
    user = request.user
    if user.role != 2:
        messages.error(request, "You do not have permission to approve this report.")
        return redirect('home')

    report = get_object_or_404(Report, id=report_id)
    report.is_visible = True
    report.approved_by = user
    report.status = True
    report.save()
    # messages.success(request, "Report approved successfully.")
    return redirect('view_pending_report')

@login_required(login_url='login')
def reportStatusUpdateView(request, report_id):
    user = request.user
    if user.role != 2:
        messages.error(request, "You do not have permission to update the status of this report.")
        return redirect('home')

    report = get_object_or_404(Report, id=report_id)
    report.status = True
    report.save()
    # messages.success(request, "Report status updated successfully.")
    return redirect('view_all_reports')

@login_required(login_url='login')
def reportStatusUpdatePending(request, report_id):
    user = request.user
    if user.role != 2:
        messages.error(request, "You do not have permission to update the status of this report.")
        return redirect('home')

    report = get_object_or_404(Report, id=report_id)
    report.status = True
    report.save()
    # messages.success(request, "Report status updated successfully.")
    return redirect('view_pending_report')