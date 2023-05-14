from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('<int:user_id>/', views.UserView.as_view(), name='user_view'),
    path('signup/', views.SignUp.as_view(), name="sign_up"),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile_view/<int:user_id>/', views.ProfileView.as_view(), name="profile-view"),
    path('get-auth-code/', views.GetAuthCode.as_view(), name="get-auth-code"),
]
