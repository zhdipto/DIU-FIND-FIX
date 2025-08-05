from datetime import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from lostfound.models import Claim, Post
from reports.models import Report
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.db.models.functions import TruncMonth

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

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

        # Field validation
        if not all([student_name, student_id, email, phone_number, birth_date, gender, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if not (email.endswith('@s.diu.edu.bd') or email.endswith('@diu.edu.bd')):
            messages.error(request, 'Please use your university email address')
            return redirect('register')

        if User.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already exists')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
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

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('home')

    return render(request, 'registration/registration.html')

def loginCheck(request):
    if request.method == 'POST':
        username = request.POST.get('id')  # Can be student_id or employee_id
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ Add success message
            messages.success(request, f"Welcome back, {user.name}!")
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
    lost_posts = Post.objects.filter(post_type='Lost', is_visible=True).order_by('-created_at')[:3]
    found_posts = Post.objects.filter(post_type='Found', is_visible=True).order_by('-created_at')[:3]

    my_posts = Post.objects.filter(user=student, is_visible=True).count()
    my_reports = Report.objects.filter(user=student, is_visible=True).count()
    pending_posts = Post.objects.filter(user=student, is_visible=False).count()
    my_claims = Claim.objects.filter(claimed_by=student, post__post_type='Found').count()
    context = {
        "student": student,
        "classActiveDashboard": "active",
        "lost_posts": lost_posts,
        "found_posts": found_posts,
        "my_posts": my_posts,
        "my_reports": my_reports,
        "pending_posts": pending_posts,
        "my_claims": my_claims,
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
        user_name = request.POST.get('name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        birth_date = request.POST.get('birth_date', '').strip()
        gender = request.POST.get('gender', '').strip()
        profile_photo = request.FILES.get('profile_photo')
        password = request.POST.get('password')

        errors = []

        # Validation
        if phone_number:
            if not phone_number.isdigit():
                errors.append("Phone number must contain only digits.")
            elif len(phone_number) < 10:
                errors.append("Phone number must be at least 10 digits.")

        if gender and gender not in ['Male', 'Female']:
            errors.append("Invalid gender selected.")

        if password and len(password) < 8:
            errors.append("Password must be at least 8 characters long.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/profile.html', {
                'user': user,
                'input_data': {
                    'user_name': user_name,
                    'phone_number': phone_number,
                    'birth_date': birth_date,
                    'gender': gender,
                }
            })

        # Update user fields
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
        if password:
            user.set_password(password)

        user.last_updated_by = request.user
        user.save()
        messages.success(request, 'Profile updated successfully')

        # Important: if password changed, re-authenticate is needed (optional)
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
    posts = Post.objects.all().filter(user=user).order_by('-created_at')

    if selected_post_type in ['lost', 'found']:
        posts = posts.filter(post_type=selected_post_type)

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

@login_required(login_url='login')
def viewStudentList(request):
    user = request.user
    if user.role not in [2, 3]:  # Ensure the user is a Super Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    students = User.objects.filter(role=1).order_by('-date_joined')
    context = {
        "classActiveStudent": "active",
        "students": students,
    }
    return render(request, 'superAdmin/viewStudentList.html', context)

@login_required(login_url='login')
def editStudentInfo(request, student_id):
    user = request.user
    if user.role not in [2, 3]:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    student = get_object_or_404(User, id=student_id)

    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        student_id_input = request.POST.get('student_id', '').strip()
        birth_date = request.POST.get('birth_date', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        gender = request.POST.get('gender', '').strip()
        profile_photo = request.FILES.get('profile_photo')
        password = request.POST.get('password')
        
        errors = []
        
        # Validation
        if email and '@' not in email:
            errors.append("Please enter a valid email address.")
        
        if phone_number:
            if not phone_number.isdigit():
                errors.append("Phone number must contain only digits.")
            elif len(phone_number) < 10:
                errors.append("Phone number must be at least 10 digits.")
        
        if gender and gender not in ['Male', 'Female']:
            errors.append("Invalid gender selected.")
        
        # Check if email exists for other users
        if email and User.objects.filter(email=email).exclude(id=student.id).exists():
            errors.append("Email already exists for another user.")
        
        # Check if student_id exists for other users
        if student_id_input and User.objects.filter(student_id=student_id_input).exclude(id=student.id).exists():
            errors.append("Student ID already exists for another user.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/editProfile.html', {
                'student': student,
                'input_data': {
                    'name': name,
                    'email': email,
                    'student_id': student_id_input,
                    'birth_date': birth_date,
                    'phone_number': phone_number,
                    'gender': gender,
                }
            })
        
        # Update student fields
        if name:
            student.name = name
        if email:
            student.email = email
        if student_id_input:
            student.student_id = student_id_input
            student.username = student_id_input
        if birth_date:
            student.birth_date = birth_date
        if phone_number:
            student.phone_number = phone_number
        if gender:
            student.gender = gender
        if profile_photo:
            student.profile_photo = profile_photo
        if password:
            student.set_password(password)

        student.last_updated_by = request.user
        student.save()
        messages.success(request, 'Student updated successfully.')
        return redirect('edit_student_info', student_id=student.id)
    context = {
        "classActiveStudent": "active",
        "student": student,
    }
    
    return render(request, 'accounts/editProfile.html',context)


@login_required(login_url='login')
def deleteStudent(request, student_id):
    user = request.user
    if user.role not in [2, 3]:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    student = get_object_or_404(User, id=student_id)
    student.delete()
    messages.success(request, 'Student deleted successfully.')
    return redirect('view_student_list')

@login_required(login_url='login')
def viewAdminList(request):
    user = request.user
    if user.role != 3:  # Ensure the user is a Super Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    employees = User.objects.filter(role=2).order_by('-date_joined')
    context = {
        "classActiveAdmin": "active",
        "admin": employees,
    }
    return render(request, 'superAdmin/viewAdminList.html', context)

@login_required(login_url='login')
def editAdminInfo(request, employee_id):
    user = request.user
    if user.role != 3:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    admin = get_object_or_404(User, id=employee_id)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        employee_id_input = request.POST.get('employee_id', '').strip()
        birth_date = request.POST.get('birth_date', '').strip()
        phone_number = request.POST.get('phone_number', '').strip
        gender = request.POST.get('gender', '').strip()
        profile_photo = request.FILES.get('profile_photo')
        password = request.POST.get('password')  

        errors = []
        
        # Validation        
        if email and '@' not in email:
            errors.append("Please enter a valid email address.")
        
        if phone_number:
            if not phone_number.isdigit():
                errors.append("Phone number must contain only digits.")
            elif len(phone_number) < 10:
                errors.append("Phone number must be at least 10 digits.")
        
        if gender and gender not in ['Male', 'Female']:
            errors.append("Invalid gender selected.")
        
        # Check if email exists for other users
        if email and User.objects.filter(email=email).exclude(id=admin.id).exists():
            errors.append("Email already exists for another user.")

        # Check if employee_id exists for other users
        if employee_id_input and User.objects.filter(employee_id=employee_id_input).exclude(id=admin.id).exists():
            errors.append("Employee ID already exists for another user.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/editProfile.html', {
                'admin': admin,
                'input_data': {
                    'name': name,
                    'email': email,
                    'employee_id': employee_id_input,
                    'birth_date': birth_date,
                    'phone_number': phone_number,
                    'gender': gender,
                }
            })
        
        # Update student fields
        if name:
            admin.name = name
        if email:
            admin.email = email
        if employee_id_input:
            admin.student_id = employee_id_input
        if birth_date:
            admin.birth_date = birth_date
        if phone_number:
            admin.phone_number = phone_number
        if gender:
            admin.gender = gender
        if profile_photo:
            admin.profile_photo = profile_photo
        if password:
            admin.set_password(password)

        admin.last_updated_by = request.user
        admin.save()
        messages.success(request, 'Admin updated successfully.')
        return redirect('edit_admin_info', employee_id=admin.id)
    context = {
        "classActiveAdmin": "active",
        "student": admin,
    }
    
    return render(request, 'accounts/editProfile.html',context)

@login_required(login_url='login')
def deleteAdmin(request, employee_id):
    user = request.user
    if user.role != 3:  # Ensure the user is a Super Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    admin = get_object_or_404(User, id=employee_id)
    admin.delete()
    messages.success(request, 'Admin deleted successfully.')
    return redirect('view_admin_list')

@login_required(login_url='login')
def adminDashboard(request):
    user = request.user
    if user.role != 2:  # Ensure the user is an Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    # Bar Chart Data: Monthly Post Counts
    monthly_posts = (
        Post.objects.filter(is_visible=True)
        .annotate(month=TruncMonth('event_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    months = [entry['month'].strftime('%B') for entry in monthly_posts]  # E.g., ['January', 'February', ...]
    post_counts = [entry['count'] for entry in monthly_posts]            # E.g., [5, 10, ...]

    # Pie Chart Data: Post Type Distribution
    type_counts = (
        Post.objects.filter(is_visible=True)
        .values('post_type')
        .annotate(count=Count('id'))
    )

    post_type_labels = [entry['post_type'].capitalize() for entry in type_counts]  # ['Lost', 'Found']
    post_type_counts = [entry['count'] for entry in type_counts]

    current_year = datetime.now().year
    monthly_report_counts = (
        Report.objects.filter(is_visible=True,event_date__year=current_year)
        .annotate(month=TruncMonth('event_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Prepare data for chart
    report_month_labels = []
    report_month_data = []

    for month_data in monthly_report_counts:
        month_name = month_data['month'].strftime('%B')  # e.g., "January"
        report_month_labels.append(month_name)
        report_month_data.append(month_data['count'])  

    
    approved_posts = Post.objects.filter(is_visible=True,approved_by_id=user).count()
    pending_posts = Post.objects.filter(is_visible=False).count()
    pending_reports = Report.objects.filter(is_visible=False).count()
    claimed_items = Claim.objects.filter(verified_by_id=user.id).count()

    context = {
        "classActiveDashboard": "active",
        "user": user,
        'months': months,
        'post_counts': post_counts,
        'post_type_labels': post_type_labels,
        'post_type_counts': post_type_counts,
        'report_month_labels': report_month_labels,
        'report_month_data': report_month_data,
        'approved_posts': approved_posts,
        'pending_posts': pending_posts,
        'pending_reports': pending_reports,
        'claimed_items': claimed_items,
    }
    return render(request, 'Admin/adminDashboard.html', context)

@login_required(login_url='login')
def viewMyClaims(request):
    user = request.user
    if user.role != 1:  # Ensure the user is an Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    my_claims = Claim.objects.filter(claimed_by=user, post__post_type='Found')

    context = {
        "classActiveDashboard": "active",
        "my_claims": my_claims,
    }

    return render(request, 'student_dashboard_content/myClaim.html', context)