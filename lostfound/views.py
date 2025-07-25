from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='loginCheck')
def viewFoundItem(request):
    # This view will render the found item page
    context = {
        "classActiveViewAllItem": "active",
        "classActiveViewFoundItem": "active",
    }
    return render(request, 'foundItem/viewFoundItem.html', context)

@login_required(login_url='loginCheck')
def viewLostItem(request):
    # This view will render the found item page
    context = {
        "classActiveViewAllItem": "active",
        "classActiveViewLostItem": "active",
    }
    return render(request, 'lostItem/viewLostItem.html', context)

@login_required(login_url='loginCheck')
def createPost(request):
    # This view will render the create post page
    context = {
        "classActiveCreatePost": "active",
    }
    return render(request, 'post/createPost.html', context)