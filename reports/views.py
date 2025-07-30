from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from reports.models import Report

# Create your views here.
@login_required(login_url='loginCheck')
def viewAllReports(request):
    # This view will render the page to view all reports
    selected_location = request.GET.get('location') 
    if selected_location:
        report = Report.objects.filter(
            is_visible=False,
            location__iexact=selected_location
        ).order_by('-submitted_at')
    else:
        report = Report.objects.filter(
            is_visible=False
        ).order_by('-submitted_at')
    context = {
        "classActiveReports": "active",
        "classActiveViewAllReports": "active",
        "reports": report,
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
            user=request.user,
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