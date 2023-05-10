from django.db import models
from users.models import models

# # 게시글 모델
# class Post(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=50)
#     content = models.TextField()
#     image = models.ImageField(blank=True, upload_to='%Y/%m/')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.title)
 
# # 좋아요 모델 추가

