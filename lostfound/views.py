from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Claim, Post
from users.models import User
from django.db.models import Exists, OuterRef
# Create your views here.


LOCATIONS = [
        ('Inspiration (AB-01)', 'Inspiration (AB-01)'),
        ('Scholars\' Home (AB-03)', 'Scholars\' Home (AB-03)'),
        ('Falcon (AB-02)', 'Falcon (AB-02)'),
        ('Knowledge Tower (AB-04)', 'Knowledge Tower (AB-04)'),
        ('Knowledge Valley', 'Knowledge Valley'),
        ('E.Complex Playground', 'E.Complex Playground'),
        ('DIU Security Shade', 'DIU Security Shade'),
        ('EEE Building', 'EEE Building'),
        ('DIU Central Store', 'DIU Central Store'),
        ('Textile Lab Building', 'Textile Lab Building'),
        ('Civil Building', 'Civil Building'),
        ('Admission Office', 'Admission Office'),
        ('Auditorium', 'Auditorium'),
        ('Swimming Pool', 'Swimming Pool'),
        ('Central Playground', 'Central Playground'),
        ('DIU Golf Field', 'DIU Golf Field'),
        ('Basketball Court', 'Basketball Court'),
        ('Green Garden Restaurant', 'Green Garden Restaurant'),
        ('Python Road', 'Python Road'),
        ('Central Mosque', 'Central Mosque'),
        ('Innovation Lab', 'Innovation Lab'),
        ('Studio Apartment', 'Studio Apartment'),
        ('Practice Playground', 'Practice Playground'),
        ('Vehicle Parking 01', 'Vehicle Parking 01'),
        ('Vehicle Parking 02', 'Vehicle Parking 02'),
        ('Campus Store & Food Court', 'Campus Store & Food Court'),
        ('Gymnasium', 'Gymnasium'),
        ('Staff Quarter', 'Staff Quarter'),
        ('Daffodil Lake Area', 'Daffodil Lake Area'),
        ('DIU Garden', 'DIU Garden'),
        ('YKSG-02 (A)', 'YKSG-02 (A)'),
        ('YKSG-02 (B)', 'YKSG-02 (B)'),
        ('RASG-01', 'RASG-01'),
        ('RASG-02', 'RASG-02'),
        ('Bonomaya', 'Bonomaya'),
        ('Teflon Chattar', 'Teflon Chattar'),
        ('DIU Airplane', 'DIU Airplane'),
        ('DIU Bridge', 'DIU Bridge'),
        ('Anisul Haque Bhaban', 'Anisul Haque Bhaban'),
        ('Teachers Dormitory 01', 'Teachers Dormitory 01'),
        ('Teachers Dormitory 02', 'Teachers Dormitory 02'),
        ('Transport Parking - 01', 'Transport Parking - 01'),
        ('Transport Office', 'Transport Office'),
        ('Shaheed Minar', 'Shaheed Minar'),
        ('YKSG-01 (A)', 'YKSG-01 (A)'),
        ('YKSG-01 (B)', 'YKSG-01 (B)'),
        ('YKSG-01 (Play Ground)', 'YKSG-01 (Play Ground)'),
        ('Labour Shade', 'Labour Shade'),
        ('Dairy Farm', 'Dairy Farm'),
        ('Nishat Kabor Hall', 'Nishat Kabor Hall'),
        ('Daffodil Institute of Social Science (DISS)', 'Daffodil Institute of Social Science (DISS)'),
        ('Gate 01 (South)', 'Gate 01 (South)'),
        ('Gate 02 (South)', 'Gate 02 (South)'),
        ('Gate 03 (South)', 'Gate 03 (South)'),
        ('Gate 04 (West)', 'Gate 04 (West)'),
        ('Gate 05 (West)', 'Gate 05 (West)'),
        ('Gate 06 (North)', 'Gate 06 (North)'),
        ('Gate 07 (North)', 'Gate 07 (North)'),
        ('Gate 08 (East)', 'Gate 08 (East)'),
        ('Gate 09 (East)', 'Gate 09 (East)'),
    ]
@login_required(login_url='login')
def viewFoundItem(request):
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
    lost_posts = Post.objects.filter(
            post_type='lost',
            is_visible=True
        ).prefetch_related('claim_set').order_by('-created_at')

    context = {
        "classActiveViewAllItem": "active",
        "classActiveViewLostItem": "active",
        "lost_posts": lost_posts,
    }
    return render(request, 'lostItem/viewLostItem.html', context)



@login_required(login_url='login')
def createPost(request):
    user = request.user
    if request.method == 'POST':
        itemName = request.POST.get('itemName')
        description = request.POST.get('description')
        location = request.POST.get('location')
        event_date = request.POST.get('date')
        event_time = request.POST.get('time')
        photo = request.FILES.get('photo')
        post_type = request.POST.get('post_type')
        username = request.POST.get('username')

        if user.role == 2:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return redirect('create_post')

        post = Post.objects.create(  
            user=user,
            item_name=itemName,
            description=description,
            location=location,
            photo=photo,
            event_date=event_date,
            event_time=event_time,
            created_at=timezone.now(),
            is_visible=False,
            post_type=post_type
        )
        post.save()
        messages.success(request, 'Post created successfully and is pending for approval.')
        return redirect('create_post')

    context = {
        "classActiveCreatePost": "active",
        "user": user,
        "location": LOCATIONS,
    }
    return render(request, 'post/createPost.html', context)

@login_required(login_url='login')
def viewPendingPost(request):
    user = request.user
    if user.role != 2:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    selected_post_type = request.GET.get('post_type')
    posts = Post.objects.all().filter(is_visible=False).order_by('-created_at')

    if selected_post_type in ['lost', 'found']:
        posts = posts.filter(is_visible=False, post_type=selected_post_type).order_by('-created_at')

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

        messages.success(request, 'Post updated successfully')
        return redirect('edit_post', post_id=post.id)
    context = {
        "classActiveCreatePost": "active",
        "post": post,
        "locations" : LOCATIONS
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
    messages.success(request, 'Post deleted successfully')
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
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
    messages.success(request, 'Post approved')
    return redirect('view_pending_post')

@login_required(login_url='login')
def adminApprovePost(request):
    user = request.user
    if user.role != 2:  # Ensure the user is an Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    selected_post_type = request.GET.get('post_type')
    posts = Post.objects.all().filter(is_visible=True, approved_by=user).order_by('-created_at')

    if selected_post_type in ['lost', 'found']:
        posts = posts.filter(is_visible=True, approved_by=user, post_type=selected_post_type).order_by('-created_at')
    
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
    
    claimed_items = Claim.objects.all()
    
    # 🔍 Filter by post_type from the Post model using relationship
    if post_type:
        claimed_items = claimed_items.filter(post__post_type=post_type)
     
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

        if post.post_type == 'found':
            post.status = True
            claim.status = True
            messages.success(request, 'Item claimed successfully')
        post.save()
        claim.save()
        return redirect('claim_item_list')
    
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
    claims = Claim.objects.all().filter(verified_by_id=user.id).order_by('-claimed_at')

    if selected_post_type in ['lost', 'found']:
        claims = claims.filter(post__post_type=selected_post_type)

    context = {
        "classActiveDashboard": "active",
        "claims": claims
    }
    return render(request, 'post/adminVerifiedClaim.html', context)

@login_required(login_url='login')
def deleteClaim(request, claim_id):
    user = request.user
    if user.role != 2:  # Ensure the user is a Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    claim = get_object_or_404(Claim, id=claim_id)
    claim.delete()
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('claim_item_list')

@login_required(login_url='login')
def approveClaim(request, claim_id):
    user = request.user
    if user.role != 2:  # Ensure the user is a Admin
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    claim = get_object_or_404(Claim, id=claim_id)
    claim.post.status = True
    claim.post.save()
    claim.status = True
    claim.verified_by = user
    claim.save()
    messages.success(request, 'Item Returned successfully')

    return redirect('claim_item_list')