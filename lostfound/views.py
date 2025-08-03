from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Claim, Post
from users.models import User
# Create your views here.

@login_required(login_url='login')
def viewFoundItem(request):
    # This view will render the found item page
    selected_location = request.GET.get('location')  # Get location from query param
    if selected_location:
        found_posts = Post.objects.filter(
            post_type='found',
            is_visible=True,
            location__iexact=selected_location
        ).order_by('-created_at')
    else:
        found_posts = Post.objects.filter(
            post_type='found',
            is_visible=True
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
            is_visible=True,
            location__iexact=selected_location
        ).order_by('-created_at')
    else:
        lost_posts = Post.objects.filter(
            post_type='lost',
            is_visible=True
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
    posts = Post.objects.none()

    if selected_post_type == 'lost':
        posts = Post.objects.filter(is_visible=False, post_type='lost').order_by('-created_at')
    elif selected_post_type == 'found':
        posts = Post.objects.filter(is_visible=False, post_type='found').order_by('-created_at')

    context = {
        "classActiveViewAllItem": "active",
        "classActiveViewPendingPost": "active",
        "posts": posts,
    }
    return render(request, 'post/viewPendingPost.html', context)

@login_required(login_url='login')
def editPost(request, post_id):
    user = request.user
    if user.role != 2:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        item_name = request.POST.get('itemName')
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

@login_required(login_url='login')
def deletePost(request, post_id):
    user = request.user
    if user.role != 2:  # Ensure the user is an Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('view_pending_post')

@login_required(login_url='login')
def approvePost(request, post_id):
    user = request.user
    if user.role != 2:  # Ensure the user is an Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    post = get_object_or_404(Post, id=post_id)
    post.is_visible = True
    post.approved_by = user
    post.save()
    return redirect('view_pending_post')

@login_required(login_url='login')
def adminApprovePost(request):
    user = request.user
    if user.role != 2:  # Ensure the user is an Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    selected_post_type = request.GET.get('post_type')
    posts = Post.objects.none()

    if selected_post_type == 'lost':
        posts = Post.objects.filter(is_visible=True, approved_by=user, post_type='lost').order_by('-created_at')
    elif selected_post_type == 'found':
        posts = Post.objects.filter(is_visible=True, approved_by=user, post_type='found').order_by('-created_at')

    
    context = {
        "classActiveDashboard": "active",
        "posts": posts,
    }
    return render(request, 'post/adminApprovedPost.html', context)

@login_required(login_url='login')
def claimItemList(request):
    user = request.user
    if user.role != 2:  # Only admin can access
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    post_type = request.GET.get('post_type')  # 'lost' or 'found'
    post_id = request.GET.get('post_id')  # ID of the post
    
    claimed_items = Claim.objects.all()
    
    # 🔍 Filter by post_type from the Post model using relationship
    if post_type:
        claimed_items = claimed_items.filter(post__post_type=post_type)
    
    # 🔍 Filter by specific post ID
    if post_id:
        claimed_items = claimed_items.filter(post=post_id)
    
    context = {
        "classActiveViewAllItem": "active",
        "classActiveClaimItem": "active",
        "claimed_items": claimed_items
    }
    return render(request, 'post/claimItemList.html', context)

@login_required(login_url='login')
def claimItem(request, post_id):
    user = request.user
    if user.role != 2:  # Ensure the user is a Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        message = request.POST.get('message', '')
        entered_student_id = request.POST.get('claimed_by_id')

        try:
            # Use username or your custom student_id field
            student_user = User.objects.get(username=entered_student_id)
        except User.DoesNotExist:
            messages.error(request, f"No student found with ID {entered_student_id}.")
            return redirect('lostfound_detail', post_id=post.id)
    
        claim = Claim.objects.create(
            post=post,
            claimed_by=student_user,
            message=message,
            claimed_at=timezone.now(),
            verified_by=user
        )
        claim.save()
        post.status = True
        post.save()
        return redirect('claim_item_list', post_id=post.id)

    context = {
        "classActiveClaimItem": "active",
        "post": post
    }
    return render(request, 'post/claimItem.html', context)

@login_required(login_url='login')
def adminVerifiedClaim(request):
    user = request.user
    if user.role != 2:  # Ensure the user is a Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    selected_post_type = request.GET.get('post_type')
    claims = Claim.objects.none()

    if selected_post_type == 'lost':
        claims = Claim.objects.filter(verified_by_id=user.id, post__post_type='lost').order_by('-claimed_at')

    elif selected_post_type == 'found':
        claims = Claim.objects.filter(verified_by_id=user.id, post__post_type='found').order_by('-claimed_at')
    
    context = {
        "classActiveDashboard": "active",
        "claims": claims
    }
    return render(request, 'post/adminVerifiedClaim.html', context)