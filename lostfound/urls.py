from django.urls import path
from . import views


urlpatterns = [
    path('view-found-item/', views.viewFoundItem, name='view_found_item'),
    path('view-lost-item/', views.viewLostItem, name='view_lost_item'),
    path('create-post/', views.createPost, name='create_post'),
    path('view-pending-post/', views.viewPendingPost, name='view_pending_post'),
    path('edit-post/<int:post_id>/', views.editPost, name='edit_post'),
]