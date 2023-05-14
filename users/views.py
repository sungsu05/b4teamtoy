from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (UserSerializer, ComtomTokenObtainPairSerializer, ReadUserSerializer,
                          ReadProfileSerializer, UpdateProfileSerializer, GetFollowInfoSerializer)
from django.core.mail import EmailMessage
import random


# 회원 가입


<<<<<<< HEAD
class AuthFuntion():
    def send_mail(self, email):
=======
class AuthFunction():
    def send_mail(self,email):
>>>>>>> 9d1998601a6fde37d7669031b8f7a78a5582ed1e
        code = "".join([str(random.randrange(0, 10)) for i in range(6)])
        title = "B4GAMES 가입 인증 코드 발송"
        content = f"인증 코드 = {code}"
        mail = EmailMessage(title, content, to=[email])
        mail.send()

        # 올바른 이메일로 발송했는지 검증 절차 필요
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


<<<<<<< HEAD
class SignUp(APIView, AuthFuntion):
    def send_mail(self, email):
=======
class SignUp(APIView,AuthFunction):
    def send_mail(self,email):
>>>>>>> 9d1998601a6fde37d7669031b8f7a78a5582ed1e
        code = "".join([str(random.randrange(0, 10)) for i in range(6)])
        title = "B4GAMES 가입 인증 코드 발송"
        content = f"인증 코드 = {code}"
        mail = EmailMessage(title, content, to=[email])
        mail.send()

        # 올바른 이메일로 발송했는지 검증 절차 필요
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
        print(owner.auth_code)
        if owner.auth_code == request.data['auth_code']:
            owner.is_active = True
            owner.save()
            return Response({"message": "인증되셨습니다."}, status=status.HTTP_200_OK)

        return Response({"error": "인증 코드가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

<<<<<<< HEAD

class UserView(APIView, AuthFuntion):
=======
class UserView(APIView,AuthFunction):
>>>>>>> 9d1998601a6fde37d7669031b8f7a78a5582ed1e
    # 회원 정보 읽기
    def get(self, request, user_id):
        owner = get_object_or_404(User, id=user_id)
        serializer = ReadUserSerializer(owner)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 회원 정보 수정
    def put(self, request, user_id):
        if not self.check_password(request.data['password']):
            return Response({'error': '비밀번호가 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        owner = get_object_or_404(User, id=user_id)
        print(owner.auth_code)
        if not request.data['auth_code'] == owner.auth_code:
            return Response({'error': '인증 코드가 올바르지 않습니다.'}, status=status.HTTP_421_MISDIRECTED_REQUEST)

        if request.user == owner:
            serializer = UserSerializer(owner,data=request.data,partial=True)
            # partial=True : 부분 업데이트
            if serializer.is_valid():
                serializer.save()

                update_user_info = ReadUserSerializer(owner)
                return Response(update_user_info.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 휴면 계정으로 전환
    def delete(self, request, user_id):
        owner = get_object_or_404(User, id=user_id)
        if request.user == owner:
            owner = get_object_or_404(User, id=user_id)
            owner.is_active = False
            owner.save()
            return Response({"message": "휴면 계정으로 전환되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = ComtomTokenObtainPairSerializer


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

    # owner가 자신의 프로필을 수정
    def put(self, request, user_id):
        owner = get_object_or_404(User, id=user_id)
        if request.user == owner:
            serializer = UpdateProfileSerializer(owner, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                update_profile_info = ReadProfileSerializer(owner)
                return Response(update_profile_info.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

<<<<<<< HEAD

class GetAuthCode(APIView, AuthFuntion):
    def post(self, request):
        owner = get_object_or_404(User, email=request.data['email'])
        owner.auth_code = self.send_mail(owner.email)
        owner.save()
        print(owner.auth_code)
        return Response({"message": "인증 메일을 발송 했습니다."}, status=status.HTTP_200_OK)
=======
class GetAuthCode(APIView,AuthFunction):
    def post(self,request):
        owner = get_object_or_404(User,email=request.data['email'])
        owner.auth_code = self.send_mail(owner.email)
        owner.save()
        print(owner.auth_code)
        return Response({"message":"인증 메일을 발송 했습니다."}, status=status.HTTP_200_OK)
>>>>>>> 9d1998601a6fde37d7669031b8f7a78a5582ed1e
