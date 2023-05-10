from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함

class UserManager(BaseUserManager):
    def create_user(self,email,username,nickname,is_seller,password=None):
        is_seller = is_seller.upper()

        if not username:
            raise ValueError('사용자 이름은 필수 입력 사항 입니다.')
        elif not password:
            raise ValueError('사용자 비밀번호는 필수 입력 사항 입니다.')
        # elif not nickname:
        #     raise ValueError('사용자 별명은 필수 입력 사항 입니다.')
        # elif not email:
        #     raise ValueError('사용자 이메일은 필수 입력 사항 입니다.')
        # elif is_seller == None:
        #     raise ValueError('사용자 판매/일반 회원 여부는 필수 선택 사항 입니다.')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            nickname=nickname,
            is_seller=is_seller,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self,email,username,nickname,is_seller,password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
            nickname=nickname,
            is_seller=is_seller,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# name, password, nickname, email, follow, created_at, updated_at, signout_at, is_active, is_seller
class User(AbstractBaseUser):
    username = models.CharField("사용자 이름", max_length=20)
    password = models.CharField("비밀번호", max_length=128) # max?
    nickname = models.CharField("닉네임", max_length=20,unique = True)
    email = models.EmailField("이메일 주소", max_length=100,unique = True)
    created_at = models.DateTimeField("가입일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    signout_at = models.DateTimeField("탈퇴일", auto_now_add=True)
    follow = models.ManyToManyField('self',symmetrical=False,related_name='followers',blank=True)

    SELLER_CHOICE =(
        # seller or  member
        ('S','판매 회원'),  # 판매 회원
        ('M','일반 회원'), # 일반 회원
    )
    is_seller = models.CharField(max_length=10,choices=SELLER_CHOICE)

    # is_staff에서 해당 값 사용
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # id로 사용 할 필드 지정.
    # 로그인 시 USERNAME_FIELD에 설정 된 필드와 password가 사용된다.\
    USERNAME_FIELD = 'nickname'
    # USERNAME_FIELD = 'username'

    # user를 생성할 때 입력받은 필드 지정
    REQUIRED_FIELDS = ['username','email','is_seller']
    objects = UserManager()  # custom user 생성 시 필요

    def __str__(self):
        return self.username

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True

    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    # is_seller 권한 설정
    # @property
    # def is_selleruser(self):
    #     return self.is_seller
