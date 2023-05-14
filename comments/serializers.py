from rest_framework import serializers
from comments.models import Comment




class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
 
    
    def get_owner(self, obj):
        return obj.owner.username
    
    class Meta:
        model = Comment
        fields = "__all__"   

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
    


