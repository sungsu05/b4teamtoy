from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','nickname','email','is_seller',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
        extra_kwargs = {
            "password": {"write_only": True},
            # 이메일 인증 기능
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
        # 비밀번호 복호화
        user.set_password(user.password)
        user.save()
        return user

        # 회원 정보 수정, 오버라이딩
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        # 비밀번호 복호화
        user.set_password(user.password)
        user.save()
        return user

class ComtomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['nickname'] = user.nickname
        token['is_seller'] = user.is_seller
        return token
