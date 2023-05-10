from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from users.models import User


class UserView(APIView):
    def get(self, request):
        user = request.user
        serialized_user_data = UserSerializer(user).data
        return Response(serialized_user_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """ 사용자 정보 등록 """
        serialized_user = UserSerializer(request.data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response({"message": "가입완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serialized_user.errors}"}, status=status.HTTP_400_BAD_REQUEST)
      
    def put(self, request):
        """ 사용자 정보 수정 """
        return Response({"message": "user put"})
    
    def delete(self, request):
        """ 회원 탈퇴 """
        return Response({"message": "user delete"})
    
class CustomTokenObtainPairView(TokenObtainPairView, TokenVerifyView):
    serializer_class = CustomTokenObtainPairSerializer
