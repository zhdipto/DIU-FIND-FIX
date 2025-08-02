from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from users.models import User
# Create your views here.

@login_required(login_url='login')
def viewFoundItem(request):
    # This view will render the found item page
    selected_location = request.GET.get('location')  # Get location from query param
    if selected_location:
        found_posts = Post.objects.filter(
            post_type='found',
            is_visible=False,
            location__iexact=selected_location
        ).order_by('-created_at')
    else:
        found_posts = Post.objects.filter(
            post_type='found',
            is_visible=False
        ).order_by('-created_at')

    context = {
        "classActiveViewAllItem": "active",
        "classActiveViewFoundItem": "active",
        "found_posts": found_posts,
    }
    return render(request, 'foundItem/viewFoundItem.html', context)

@login_required(login_url='login')
def viewLostItem(request):
    # Fetch all visible lost posts
    selected_location = request.GET.get('location')  # Get location from query param

    if selected_location:
        lost_posts = Post.objects.filter(
            post_type='lost',
            is_visible=False,
            location__iexact=selected_location
        ).order_by('-created_at')
    else:
        lost_posts = Post.objects.filter(
            post_type='lost',
            is_visible=False
        ).order_by('-created_at')

    context = {
        "classActiveViewAllItem": "active",
        "classActiveViewLostItem": "active",
        "lost_posts": lost_posts,
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
            user=request.user,  # ForeignKey to Student
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
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    context = {
        "classActiveCreatePost": "active",
        "student": user,
    }
    return render(request, 'post/createPost.html', context)

@login_required(login_url='login')
def viewPendingPost(request):
    user = request.user
    if user.role != 2:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    selected_post_type = request.GET.get('post_type')

    if selected_post_type == 'lost':
        posts = Post.objects.filter(is_visible=False, post_type='lost').order_by('-created_at')
    else:
        posts = Post.objects.filter(is_visible=False, post_type='found').order_by('-created_at')

    context = {
        "classActiveViewAllItem": "active",
        "classActiveViewPendingPost": "active",
        "posts": posts,
    }
    return render(request, 'post/viewPendingPost.html', context)

@login_required(login_url='login')
def editPost(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        item_name = request.POST.get('itemName')
        # studentId = request.POST.get('studentId')
        description = request.POST.get('description')
        location = request.POST.get('location')
        event_date = request.POST.get('date')
        event_time = request.POST.get('time')
        photo = request.FILES.get('photo')

        # Update the post
        if post_type not in ['lost', 'found']:
            messages.error(request, 'Invalid post type selected.')
            return redirect('edit_post', post_id=post.id)
        post.item_name = item_name
        post.description = description
        post.location = location
        post.event_date = event_date
        post.event_time = event_time
        post.post_type = post_type
        if photo:
            post.photo = photo
        post.last_updated_by = request.user
        post.save()
        return redirect('edit_post', post_id=post.id)
    context = {
        "classActiveCreatePost": "active",
        "post": post
    }
    return render(request, 'post/editPost.html', context)