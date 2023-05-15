# B4 teamtoy project

---

## 팀 프로젝트 개발 환경

`Python 3.11`
`Django 4.2`
`Django Rest Framework 3.14`

---

## 팀 프로젝트 소개

> **B4games**
> 재밌는 게임을 추천 소개, 공유 하는 서비스

> 컨셉 사이트

- [Epicgames](https://store.epicgames.com/)
- [Steam](https://store.steampowered.com/)

---

## [ERD](https://www.erdcloud.com/d/7KTHFPDdfAvAcpLas)

---

## 백엔드 이슈

추후 피드백을 반영하고 학습하기 위해 기록합니다

- [x] 해결 이슈
- [ ] 미결 이슈

---

- [x] profile 구현부가 serializer가 아닌 form을 사용하여 mvt pattern으로 구현됨.

```python
# profiles/forms.py
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'status']
```

```python
# profiles/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile, Follower

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 업데이트 되었습니다.')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})

def profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    following = Follower.objects.filter(user=profile.user).count()
```

> => 변경

```python
from rest_framework import serializers

...

class ReadProfileSerializer(serializers.ModelSerializer):

    followers = serializers.StringRelatedField(many=True)
    followings = serializers.StringRelatedField(many=True)
    post_count = serializers.SerializerMethodField()

    def get_post_count(self, obj):
        return obj.post_set.count()

    class Meta:
        model = User
        fields = ('username', 'email', 'followings', 'followers', 'is_seller', 'image', 'status_message','post_count')

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','image','status_message',)
```

```python
from rest_framework.views import APIView
...
class ProfileView(APIView):
    # owner의 프로필 읽기 (public)
    def get(self, request, user_id):
        owner = get_object_or_404(User, id=user_id)
        serializer = ReadProfileSerializer(owner)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # owner를 팔로우,언팔로우
    def post(self, request, user_id):
        # if not request.user.is_authenticated:
        #     return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED)

        owner = get_object_or_404(User, id=user_id)

        if request.user == owner:
            return Response("나 자신을 팔로우 할 수 없습니다.", status=status.HTTP_400_BAD_REQUEST)

        if request.user in owner.followers.all():
            owner.followers.remove(request.user)
            return Response("unfollow", status=status.HTTP_200_OK)
        else:
            owner.followers.add(request.user)
            return Response("follow", status=status.HTTP_200_OK)
```

---

- [ ] 유저모델(User)에 판매자 계정 필드`is_seller(Boolean)`를 추가하여
      유저를구분하고 회원가입을 구현했습니다. 하지만 판매자의 권한을 정의할 수 있는 shop application (`결제` or `판매`) 없는 상태입니다. 서비스의 핵심 기능을 먼저 정의하고 기획하는 부분이 중요합니다.

---

- [x] [backports.zoneinfo 0.2.1](https://pypi.org/project/backports.zoneinfo/) 개발환경을 통일하지 않고 작업 진행중 `Python 3.9`버전 미만의 환경에 설치되어 다른 버전을 사용하는 작업자와 공유 시 에러를 유발하는 헤당 package확인. 버전 통합후 해결했습니다.

  > > 팀 개발 환경 설정을 먼저 해야합니다.

---

- [x] dotenv 시크릿키가 없었기때문에 makemigrations,migrate 에러 발생 해결 방법 dotenv같은 중요한 정보가 담긴 파일은 팀원과 공유하면 됩니다.

  > > 팀원들 각자 시크릿키 재발급 받아 할 필요가 없어짐
  > > 팀원들은 각자의 파일에 .env 파일을 만들어
  > > 공유된 시크릿키를 사용합니다

---

- [x] 로그인, 로그아웃, 회원 가입같은 필수 기능이 완료 되었으나, 꼭 필요한 데이터인지 고민이 필요한 시점에 관성적으로 유저모델에 여러 필드를 추가했던 문제를 피드백받았습니다. 불필요한 데이터 필드는 삭제하였고 앞으로 모델 설계시에도 기능과 관계없는 필드는 넣지 않아야 합니다.

---

- [x] 로그인시 비밀번호 암호화, 이메일 인증기능을 추가하기 위해 모델, 뷰 재정의하였습니다 [장고 공식 문서](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#substituting-a-custom-user-model)

```python
# users/models.py
class UserManager(BaseUserManager):

    def check_password(self,password):
        check = [
            lambda element: all(
                x.isdigit() or x.islower() or x.isupper() or (x in ['!', '@', '#', '$', '%', '^', '&', '*', '_']) for x in element),
            # 요소 하나 하나를 순환하며 숫자,소문자,대문자,지정된 특수문자 제외한 요소가 있을경우 False
            lambda element: len(element) == len(element.replace(" ", "")),
            # 공백이 포함 되어 있을 경우 False
            lambda element: True if (len(element) > 7 and len(element) < 21) else False,
            # 전달된 값의 개수가 8~20 사이일 경우 True
            lambda element: any(x.islower() or x.isupper() for x in element),

        ]
        for i in check:
            if not i(password):
                return False
        return True

    def create_user(self,email,username,is_seller,password=None):

        if not self.check_password(password):
            raise ValueError('비밀번호가 올바르지 않습니다.')
        elif not username:
            raise ValueError('사용자 별명은 필수 입력 사항 입니다.')
        elif not email:
            raise ValueError('사용자 이메일은 필수 입력 사항 입니다.')
        elif is_seller == None:
            raise ValueError('사용자 판매/일반 회원 여부는 필수 선택 사항 입니다.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_seller=is_seller,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
```

```python
# users/serializers
from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from posts.models import Post

class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','is_seller',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
            # 이메일 예외 처리 메시지
            "email": {
                "error_messages": {
                "unique": "이미 존재하는 이메일입니다.",
                "invalid": "이메일 형식이 올바르지 않습니다.",
                "required": "False"
                },
            },
        }
    def create(self, validated_data):
        user = super().create(validated_data)
        # 비밀번호 해싱(암호화)
        user.set_password(user.password)
        user.save()
        return user

        # 회원 정보 수정, 오버라이딩
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        # 비밀번호 해싱(암호화)
        user.set_password(user.password)
        user.save()
        return user

class ComtomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['is_seller'] = user.is_seller
        return token
```

```python
# users/views.py
class AuthFunction():
    def send_mail(self,email):
        code = "".join([str(random.randrange(0, 10)) for i in range(6)])
        title = "B4GAMES 가입 인증 코드 발송"
        content = f"인증 코드 = {code}"
        mail = EmailMessage(title, content, to=[email])
        mail.send()

        # 올바른 이메일로 발송했는지는 확인할 수 없음
        return code

    def check_password(self, password):
        check = [
            lambda element: all(
                x.isdigit() or x.islower() or x.isupper() or (x in ['!', '@', '#', '$', '%', '^', '&', '*', '_']) for x
                in element),
            # 요소 하나 하나를 순환하며 숫자,소문자,대문자,지정된 특수문자 제외한 요소가 있을경우 False
            lambda element: len(element) == len(element.replace(" ", "")),
            # 공백이 포함 되어 있을 경우 False
            lambda element: True if (len(element) > 7 and len(element) < 21) else False,
            # 전달된 값의 개수가 8~20 사이일 경우 True
            lambda element: any(x.islower() or x.isupper() for x in element),
            # 요소 하나하나를 순환하며, 요소중 대문자 또는 소문자가 있어야함(숫자로만 가입 불가능)
        ]
        for i in check:
            if not i(password):
                return False
        return True



class SignUp(APIView,AuthFunction):
    def post(self, request):
        if not self.check_password(request.data['password']):
            return Response({'error': '비밀번호가 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # email로 인증 코드 발송, owner의 데이터베이스에 인증 코드 저장
            serializer.save()
            email = serializer.validated_data.get('email')
            owner = get_object_or_404(User, email=email)
            owner.auth_code = self.send_mail(email)
            # if owner.auth_code == None:
            #     owner.delete()
            #     return Response({'error':"이메일 정보가 올바르지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

            owner.save()

            return Response({'message': f'가입을 축하합니다.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        owner = get_object_or_404(User, email=request.data['email'])
        if owner.auth_code == request.data['auth_code']:
            owner.is_active = True
            owner.save()
            return Response({"message": "인증되셨습니다."}, status=status.HTTP_200_OK)

        return Response({"error": "인증 코드가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

```

### 회고

> 내용을 추가할 예정입니다

---
