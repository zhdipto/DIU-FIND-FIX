from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Student  # Import the Student model

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
        
        try:
            student = Student.objects.get(student_id=student_id)
            if student.check_password(password):
                # Login successful, redirect to home or dashboard
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid Student ID or password')
        except Student.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Student ID does not exist')

    return render(request, 'login/login.html', {})