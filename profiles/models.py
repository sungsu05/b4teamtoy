from django.db import models
from users.models import User
# Create your models here.
class Profile(models.Model):
    # User 모델과 일대일 관계 생성
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    # 이미지 필드 기본 디폴트값 구현 필요
    image = models.ImageField(blank=True, upload_to="%Y/%m")
    status_message = models.CharField(max_length=50,default="아직 상태 메시지가 없습니다.")
