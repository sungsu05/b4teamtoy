from django.urls import path
from comments import views

urlpatterns = [
    # path('',views.CommentView.as_view(),name='comment_view'),영주님의 경로잡기
    path("<int:post_id>/comment", views.CommentView.as_view(),name='comment_view'),
    path("<int:post_id>/comment/<int:comment_id>/", views.CommentDetailView.as_view(),name='comment_detail_view'),
]
