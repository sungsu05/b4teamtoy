from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {
                "write_only": True
        }
    }
    def create(self, validated_data):
        user = super().create(validated_data)

        # 비밀번호 복호화
        user.set_password(user.password)
        user.save()
        return user

    # 회원 정보 수정, 오버라이딩
    def update(self, instance, validated_data):
        user = super().update(instance,validated_data)
        # 비밀번호 복호화
        user.set_password(user.password)
        user.save()
        return user

    def validate(self, attrs):
        return super().validate(attrs)




class ComtomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['nickname'] = user.nickname
        token['is_seller'] = user.is_seller
        return token