from rest_framework import serializers
from .models import Profile



class ReadProfileSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    follow = serializers.SerializerMethodField()
    is_seller = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        filed = ('nickname','email','follow','is_seller','image','status_message')


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("owner",)