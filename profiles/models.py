from django.db import models
from users.models import User
# Create your models here.
class Profile(models.Model):
    # User 모델과 일대일 관계 생성
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    # 이미지 필드 기본 디폴트값 구현 필요
    image = models.ImageField(blank=True, upload_to="%Y/%m")
    status_message = models.CharField(max_length=50,blank=True)

    # 프로필 기능에 필요한것
    # 1. 사용자 정보 출력 - 시리얼 라이저 사용
    # 출력할 정보 (모두에게 공개되는 것)
    # User Model  - nickname, email, is_seller, follow
    # Profile Model - image,status_message

    # 2. 프로필 수정
    # 회원 정보 수정과는 다르게, 프로필 이미지, 상태 메시지만 수정  , 별도 시리얼라이저 생성할 것

    # 3. 팔로우 리스트 출력