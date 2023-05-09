from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from posts.models import Post
from posts.serializers import PostlistSerializer, PostCreateSerializer


# 게시글 메인, 작성 뷰(get, post)
class PostView(APIView):
    def get(self, request):
        '''메인에서 모든 게시글 가져오기'''
        posts = Post.objects.all()
        serializer = PostlistSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # permission_classes = [permissions.IsAuthenticated] # 일단 로그인한 사람만! 
    def post(self, request):
        '''게시글 작성'''
        # 지금은 익명작성 가능 -> 후에 로그인한 사람만 가능하게 수정하기 
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세보기, 수정, 삭제 뷰(get, put, delete) - 본인만 가능
class PostDetailView(APIView):
    def get(self, request, post_id):
        '''특정 게시글 조회'''
        posts = get_object_or_404(Post, id=post_id)

    
    def put(self, request, post_id):
        '''게시글 수정'''
        pass
    
    def delete(self, request, post_id):
        '''게시글 삭제'''
        pass
