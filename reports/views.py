from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from reports.models import Report

# Create your views here.
@login_required(login_url='loginCheck')
def viewAllReports(request):
    # This view will render the page to view all reports
    context = {
        "classActiveReports": "active",
        "classActiveViewAllReports": "active",
    }
    return render(request, 'viewReport/viewAllReport.html', context)

@login_required(login_url='loginCheck')
def submitReport(request):
    # This view will render the page to submit a report
    if request.method == 'POST':
        catagory = request.POST.get('issueCategory')
        description = request.POST.get('description')
        location = request.POST.get('location')
        event_date = request.POST.get('issueDate')
        event_time = request.POST.get('issueTime')
        photo = request.FILES.get('photo')

        report = Report.objects.create(
            student=request.user,
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
    
    student = request.user
    if not student.is_authenticated:
        return redirect('login')
    context = {
        "classActiveReports": "active",
        "classActiveSubmitReport": "active",
        "student": student,
    }
    return render(request, 'submitReport/createReport.html', context)