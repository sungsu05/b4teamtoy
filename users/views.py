from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (UserSerializer,ComtomTokenObtainPairSerializer,ReadUserSerializer,
                          ReadProfileSerializer,UpdateProfileSerializer,GetFollowInfoSerializer)
from datetime import datetime

# 회원 가입
class SignUp(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # 직렬화 데이터 추출 : https://stackoverflow.com/questions/47714516/how-to-get-field-value-in-the-serializer
            return Response({'message':f'가입을 축하합니다.'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    # 회원 정보 읽기
    def get(self,request,user_id):

        owner = get_object_or_404(User,id=user_id)
        serializer = ReadUserSerializer(owner)
        return Response(serializer.data,status=status.HTTP_200_OK)

    # 회원 정보 수정
    def put(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
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
            return Response({"error":"권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)

    # 휴면 계정으로 전환
    def delete(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
        if request.user == owner:
            owner = get_object_or_404(User, id=user_id)
            owner.is_active = False
            owner.save()
            return Response({"message":"휴면 계정으로 전환되었습니다."},status=status.HTTP_200_OK)
        else:
            return Response({"error":"권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = ComtomTokenObtainPairSerializer

class UpdateProfileView(APIView):
    # owner의 프로필 읽기 (public)
    def get(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
        serializer = ReadProfileSerializer(owner)
        return Response(serializer.data,status=status.HTTP_200_OK)

    # owner를 팔로우,언팔로우
    def post(self,request,user_id):
        # 로그인 인증 테스트 필요
        if not request.user.is_authenticated:
            return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED)

        owner = get_object_or_404(User,id=user_id)

        if request.user == owner:
            return Response("나 자신을 팔로우 할 수 없습니다.", status=status.HTTP_400_BAD_REQUEST)

        if request.user in owner.followers.all():
            owner.followers.remove(request.user)
            return Response("unfollow",status=status.HTTP_200_OK)
        else:
            owner.followers.add(request.user)
            return Response("follow",status=status.HTTP_200_OK)

    # owner가 자신의 프로필을 수정
    def put(self,request,user_id):
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