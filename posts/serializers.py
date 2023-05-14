from rest_framework import serializers
from posts.models import Post

'''메인에 가져오는 시리얼라이저 -> 작성자, 타이틀, 이미지만 가져옴'''
class PostlistSerializer (serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    
    def get_owner(self, obj):
        return obj.owner.username
    
    class Meta:
        model = Post
        fields = ("pk", "owner", "title", "image", "content")

'''게시글 작성, 수정용 시리얼라이저 -> 타이틀, 이미지, 내용'''
class PostCreateSerializer (serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "image", "content")


'''게시글 상세보기 시리얼라이저 -> 작성자, 타이틀, 이미지, 내용'''
class PostDetailSerializer (serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    
    def get_owner(self, obj):
        return obj.owner.username
    class Meta:
        model = Post
        fields = ("pk", "owner", "title", "image", "content")

'''마이페이지 내가 쓴 게시글만 가져오는 시리얼라이저 -> 타이틀, 이미지, 내용'''
class MyPostSerializer (serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk", "owner", "created_at", "title", "image", "content")