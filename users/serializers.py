from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname','email','is_seller',)

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
        token['nickname'] = user.nickname
        token['is_seller'] = user.is_seller
        return token


class GetFollowInfoSerializer(serializers.ModelSerializer):
    followers = serializers.StringRelatedField(many=True)
    followings = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ('followings','followers',)

class ReadProfileSerializer(serializers.ModelSerializer):

    followers = serializers.StringRelatedField(many=True)
    followings = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('nickname','email','followings','followers','is_seller','image','status_message')


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('image','status_message',)