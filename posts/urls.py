
from django.urls import path
from posts import views

urlpatterns = [
    path('', views.PostView.as_view(), name='post_view'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post_detail_view'),
    path('<int:user_id>/post/', views.MyPostListView.as_view(), name='my_post_list_view'),
    path('<int:post_id>/likes/', views.LikeView.as_view(), name='post_like_view'),
]