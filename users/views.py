from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from users.models import User
from users.serializers import UserSerializer

# for Postman testing
class UserView(APIView):
    def get(self, request):
        """ 사용자 정보 return """
        user = request.user
        return Response(UserSerializer(user.data))
    
    def post(self, request):
        """ 회원가입 """
        
        # User.objects.create(**request.data)
        serializer = UserSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=400)
        serializer.save()
        
        return Response({"message": "user post"})
    
    def put(self, request):
        """ 사용자 정보 수정 """
        return Response({"message": "user put"})
    
    def delete(self, request):
        """ 회원 탈퇴 """
        return Response({"message": "user delete"})
    
class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(request, **request.data)
        if not user:
            return Response({"error": "유효하지 않은 계정"})
        
        login(request, user)
        return Response({"message": "로그인 성공"})