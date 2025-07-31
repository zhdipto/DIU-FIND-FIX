import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from lostfound.models import Post
from reports.models import Report
from .models import User
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

        if User.objects.filter(student_id=student_id).exists():
            messages.add_message(request, messages.ERROR, 'Student ID already exists')
            return redirect('register')

        if password != confirm_password:
            messages.add_message(request, messages.ERROR, 'Passwords do not match')
            return redirect('register')

        user = User.objects.create(
            username=student_id,
            name=student_name,
            student_id=student_id,
            email=email,
            phone_number=phone_number,
            birth_date=birth_date,
            gender=gender,
        )
        user.set_password(password)
        user.save()

        return redirect('home')

    return render(request, 'registration/registration.html')
def loginCheck(request):
    if request.method == 'POST':
        username = request.POST.get('id')  # Can be student_id or employee_id
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.role == 1:  # Student
                return redirect('student_dashboard')
            elif user.role == 2:  # Admin
                return redirect('admin_dashboard')  # You must define this URL/view
            elif user.role == 3:  # Super Admin
                return redirect('super_admin_dashboard')  # You must define this URL/view
            else:
                messages.error(request, 'Role not recognized')
                return redirect('login')
        else:
            messages.error(request, 'Invalid ID or password')
            return redirect('login')

    return render(request, 'login/login.html')

@login_required(login_url='login')
def student_dashboard(request):
    student = request.user
    if student.role != 1:  # Ensure the user is a Student
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
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
def view_profile(request):
    user = request.user
    context = {
        "user": user,
        "classActiveAccount": "active",
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def profile_edit(request):
    
    user = request.user

    if request.method == 'POST':
        user_name = request.POST.get('user_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        birth_date = request.POST.get('birth_date', '').strip()
        gender = request.POST.get('gender', '').strip()
        profile_photo = request.FILES.get('profile_photo')
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))

        # Validation
        errors = []

        if user_name and not user_name.replace(" ", "").isalpha():
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
            return render(request, 'accounts/profile.html', {
                'user': user,
                'input_data': request.POST
            })

        # Only update fields that were submitted
        if user_name:
            user.name = user_name
        if phone_number:
            user.phone_number = phone_number
        if birth_date:
            user.birth_date = birth_date
        if gender:
            user.gender = gender
        if profile_photo:
            user.profile_photo = profile_photo

        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('view_profile')

    return render(request, 'accounts/profile.html', {
        'user': user
    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('home')

@login_required(login_url='login')
def viewMyPosts(request):
    user = request.user
    selected_post_type = request.GET.get('post_type')

    if selected_post_type == 'lost':
        posts = Post.objects.filter(user=user, post_type='lost').order_by('-created_at')
    else:
        posts = Post.objects.filter(user=user, post_type='found').order_by('-created_at')

    context = {
        "classActiveDashboard": "active",
        "posts": posts,
    }
    return render(request, 'student_dashboard_content/myPost.html', context)

@login_required(login_url='login')
def viewMyReports(request):
    user = request.user
    reports = Report.objects.filter(user=user).order_by('-submitted_at')

    context = {
        "classActiveDashboard": "active",
        "reports": reports,
    }
    return render(request, 'student_dashboard_content/myReport.html', context)

@login_required(login_url='login')
def superAdminDashboard(request):
    user = request.user
    if user.role != 3:  # Ensure the user is a Super Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    context = {
        "user": user,
        "total_students": User.objects.filter(role=1).count(),
        "total_admins": User.objects.filter(role=2).count(),
        "classActiveDashboard": "active",
    }
    return render(request, 'superAdmin/superAdminDashboard.html', context)

@login_required(login_url='login')
def createAdmin(request):
    user = request.user
    if user.role != 3:  # Ensure the user is a Super Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('fullName')
        employee_id = request.POST.get('employee_id')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        birth_date = request.POST.get('birthday')
        gender = request.POST.get('gender')  
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        photo = request.FILES.get('profile_photo')

        if not email.endswith('diu.edu.bd'):
            messages.add_message(request, messages.ERROR, 'Please use your university email address')
            return redirect('create_admin')

        if User.objects.filter(employee_id=employee_id).exists():
            messages.error(request, 'Employee ID already exists.')
            return redirect('create_admin')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('create_admin')

        user = User.objects.create(
            username=employee_id,
            name=name,
            employee_id=employee_id,
            email=email,
            phone_number=phone_number,
            birth_date=birth_date,
            gender=gender,
            role=2, # Admin role
            profile_photo=photo
        )
        user.set_password(password)
        user.save()

        messages.success(request, 'Admin account created successfully.')
        return redirect('create_admin')
    context = {
        "classActiveAdmin": "active",
    }
    return render(request, 'superAdmin/createAdmin.html', context)