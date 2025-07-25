from django.urls import path
from . import views


urlpatterns = [
    path('view-found-item/', views.viewFoundItem, name='view_found_item'),
    path('view-lost-item/', views.viewLostItem, name='view_lost_item'),
]