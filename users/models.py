from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함


class UserManager(BaseUserManager):
    def create_user(self, name, password, nickname, email):    
        if not name:
            raise ValueError('Users must have an username')
        if not password:
            raise ValueError('Users must have an password')
        if not nickname:
            raise ValueError('Users must have a nickname')
        if not email:
            raise ValueError('email address is required')
        
        user = self.model(
         username=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, name, password):
        user = self.create_user(
            username=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# name, password, nickname, email, follow, created_at, updated_at, signout_at, is_active, is_seller
class User(AbstractBaseUser):
    username = models.CharField("사용자 계정", max_length=20, unique=True)
    password = models.CharField("비밀번호", max_length=128)
    nickname = models.CharField("닉네임", max_length=20)
    email = models.EmailField("이메일 주소", max_length=100)
    # follow = models.ManyToManyField()
    created_at = models.DateTimeField("가입일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    # signout_at = models.DateTimeField("탈퇴일", default=None)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False) 
    
    objects = UserManager()  # custom user 생성 시 필요
    USERNAME_FIELD = 'username'

    # user를 생성할 때 입력받은 필드 지정
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        "사용자에게 특정 권한이 있습니까?"
        return True

    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label):
        "사용자에게 'app_label' 앱을 볼 수 있는 권한이 있습니까?"
        return True

    @property
    def is_staff(self):
        "사용자가 직원입니까?"
        return self.is_admin
    
    # is_seller 권한 설정
    # @property
    # def is_selleruser(self):
    #     return self.is_seller
