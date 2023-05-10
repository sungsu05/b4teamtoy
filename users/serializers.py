from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from dataclasses import field
from users.models import User

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
    # def validate(self, attrs):
    #     return super().validate(attrs) sereializer 사용해서 변경
    
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    
    def update(self, validated_data):
        password = validated_data.pop('password', None)
        if  password:
            validated_data['password'] = validated_data.pop('old_password')
            validated_data['set_password'] = password
        return validated_data
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name

        return token
