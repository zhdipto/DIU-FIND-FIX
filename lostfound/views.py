from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from users.models import Student
# Create your views here.

@login_required(login_url='login')
def viewFoundItem(request):
    # This view will render the found item page
    context = {
        "classActiveViewAllItem": "active",
        "classActiveViewFoundItem": "active",
    }
    return render(request, 'foundItem/viewFoundItem.html', context)

@login_required(login_url='login')
def viewLostItem(request):
    # This view will render the found item page
    context = {
        "classActiveViewAllItem": "active",
        "classActiveViewLostItem": "active",
    }
    return render(request, 'lostItem/viewLostItem.html', context)

@login_required(login_url='login')
def createPost(request):
    if request.method == 'POST':
        # Extracting data from POST
        itemName = request.POST.get('itemName')
        description = request.POST.get('description')
        location = request.POST.get('location')
        event_date = request.POST.get('date')
        event_time = request.POST.get('time')
        photo = request.FILES.get('photo')
        post_type = request.POST.get('post_type')

        # Create a new post
        post = Post.objects.create(
            student=request.user,  # ForeignKey to Student
            item_name=itemName,
            description=description,
            location=location,
            photo=photo,
            event_date=event_date,
            event_time=event_time,
            created_at=timezone.now(),
            is_visible=False,  # Default: pending admin approval
            post_type=post_type  # 'lost' or 'found'
        )

        post.save()

        return redirect('create_post')  # Change this to your view post list page

    # GET request: render form
    student = request.user
    context = {
        "classActiveCreatePost": "active",
        "student": student,
    }
    return render(request, 'post/createPost.html', context)

