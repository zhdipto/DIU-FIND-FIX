from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Student 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

# def login(request):
#     return render(request, 'login/login.html', {})

# def registration(request):
#     return render(request, 'registration/registration.html', {})

def register(request):
    if request.method == 'POST':
        student_name = request.POST.get('fullname')
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        birth_date = request.POST.get('birthday')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not email.endswith('.diu.edu.bd'):
            messages.add_message(request, messages.ERROR, 'Please use your university email address')
            return redirect('register')

        if Student.objects.filter(student_id=student_id).exists():
            messages.add_message(request, messages.ERROR, 'Student ID already exists')
            return redirect('register')

        if password != confirm_password:
            messages.add_message(request, messages.ERROR, 'Passwords do not match')
            return redirect('register')

        student = Student.objects.create(
            username=student_id,
            student_name=student_name,
            student_id=student_id,
            email=email,
            phone_number=phone_number,
            birth_date=birth_date,
            gender=gender,
        )
        student.set_password(password)
        student.save()

        return redirect('home')

    return render(request, 'registration/registration.html')
def loginCheck(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        
        # Use Django's authenticate to verify the user
        user = authenticate(request, username=student_id, password=password)
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            return redirect('student_dashboard')
        else:
            # If authenticate returns None, the credentials were wrong
            messages.add_message(request, messages.ERROR, 'Invalid Student ID or password')
            return redirect('loginCheck') # Redirect back to the login form

    return render(request, 'login/login.html', {})

@login_required(login_url='loginCheck')
def student_dashboard(request):
    student = request.user
    return render(request, 'pages/studentDashboard.html', {'student': student})