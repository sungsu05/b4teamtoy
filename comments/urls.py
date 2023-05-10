from django.urls import path
from comments import views

urlpatterns = [
    path("<int:post_id>/comment", views.CommentView.as_view(),name='comment_view'),
    path("<int:post_id>/comment/<int:comment_id>/", views.CommentDetailView.as_view(),name='comment_detail_view'),
]