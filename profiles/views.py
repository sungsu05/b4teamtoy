from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Profile


    # 프로필 기능에 필요한것
    # 1. 사용자 정보 출력 - 시리얼 라이저 사용 ,
    # GET 방식
    # 출력할 정보 (모두에게 공개되는 것)
    # User Model  - nickname, email, is_seller, follow
    # Profile Model - image,status_message

    # 2. 프로필 수정
    # PUT
    # 회원 정보 수정과는 다르게, 프로필 이미지, 상태 메시지만 수정  , 별도 시리얼라이저 생성할 것

    # 3. 팔로우 리스트 출력
    # GET

    # 이슈 1 번은 public 이므로 token 인증 필요 없음
    # 이슈 2,3번은 private 이므로 token 인증 필요


class ProfileView(APIView):
    def get(self,request):
        pass

class UpdateProfileView(APIView):
    def get(self,request,user_id):
        pass

    def post(self,request,user_id):
        pass