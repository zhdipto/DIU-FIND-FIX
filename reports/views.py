from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
    context = {
        "classActiveReports": "active",
        "classActiveSubmitReport": "active",
    }
    return render(request, 'submitReport/createReport.html', context)