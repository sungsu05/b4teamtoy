from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from posts.models import Post



# 게시글 메인, 작성 뷰(get, post)
class PostView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

# 게시글 상세보기, 수정, 삭제 뷰(get, put, delete)
class PostDetailView(APIView):
    def get(self, request, post_id):
        pass
    
    def put(self, request, post_id):
        pass
    
    def delete(self, request, post_id):
        pass
