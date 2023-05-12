from rest_framework import serializers
from .models import Profile
from users.models import User


class GetFollowInfoSerializer(serializers.ModelSerializer):
    followers = serializers.StringRelatedField(many=True)
    followings = serializers.StringRelatedField(many=True)

    def get_followings(self,obj):
        return obj.owner.followings.all()
    def get_followers(self,obj):
        return obj.owner.followers.all()

    class Meta:
        model = Profile
        fields = ('followings','followers',)

class ReadProfileSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    is_seller = serializers.SerializerMethodField()
    followers = serializers.StringRelatedField(many=True)
    followings = serializers.StringRelatedField(many=True)

    def get_nickname(self, obj):
        return obj.nickname

    def get_email(self, obj):
        return obj.email

    def get_is_seller(self, obj):
        return obj.is_seller


    class Meta:
        model = Profile
        fields = ('nickname','email','followings','followers','is_seller','image','status_message')


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('image','status_message',)
        # exclude = ("owner",)