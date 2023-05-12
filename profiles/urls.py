from django.urls import path
from . import views

urlpatterns = [
    path('get-profile/', views.ProfileView.as_view(), name="get-profile"),
    path('update-profile/<int:user_id>/', views.UpdateProfileView.as_view(), name="update-profile"),
]
