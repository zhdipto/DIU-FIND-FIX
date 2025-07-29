import datetime
from django.contrib import messages
from django.shortcuts import render, redirect

from lostfound.models import Post

from .models import Student 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

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
            return redirect('login') # Redirect back to the login form

    return render(request, 'login/login.html', {})

@login_required(login_url='login')
def student_dashboard(request):
    student = request.user
    lost_posts = Post.objects.filter(post_type='Lost').order_by('-created_at')[:3]
    found_posts = Post.objects.filter(post_type='Found').order_by('-created_at')[:3]
    context = {
        "student": student,
        "classActiveDashboard": "active",
        "lost_posts": lost_posts,
        "found_posts": found_posts,
    }
    return render(request, 'pages/studentDashboard.html', context)

@login_required(login_url='login')
def student_profile(request):
    student = request.user
    context = {
        "student": student,
        "classActiveAccount": "active",
    }
    return render(request, 'accounts/studentProfile.html', context)


@login_required(login_url='login')
def student_profile_edit(request):
    student = request.user

    if request.method == 'POST':
        student_name = request.POST.get('student_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        birth_date = request.POST.get('birth_date', '').strip()
        gender = request.POST.get('gender', '').strip()
        profile_photo = request.FILES.get('profile_photo')
        if request.POST.get('password'):
            student.set_password(request.POST.get('password'))

        # Validation
        errors = []

        if student_name and not student_name.replace(" ", "").isalpha():
            errors.append("Name must contain only letters.")

        if phone_number:
            if not phone_number.isdigit():
                errors.append("Phone number must contain only digits.")
            elif len(phone_number) < 10:
                errors.append("Phone number must be at least 10 digits.")

        if gender and gender not in ['Male', 'Female']:
            errors.append("Invalid gender selected.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/studentProfile.html', {
                'student': student,
                'input_data': request.POST
            })

        # Only update fields that were submitted
        if student_name:
            student.student_name = student_name
        if phone_number:
            student.phone_number = phone_number
        if birth_date:
            student.birth_date = birth_date
        if gender:
            student.gender = gender
        if profile_photo:
            student.profile_photo = profile_photo

        student.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('student_profile')

    return render(request, 'accounts/studentProfile.html', {
        'student': student
    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('home')