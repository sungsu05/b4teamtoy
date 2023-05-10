from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from posts.models import Post
from posts.serializers import PostlistSerializer, PostCreateSerializer, PostDetailSerializer


# 게시글 메인, 작성 뷰(get, post)
class PostView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        '''메인에서 모든 게시글 가져오기'''
        posts = Post.objects.all()
        serializer = PostlistSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 로그인한 사람만! 
    def post(self, request):
        '''게시글 작성'''
        if not request.user.is_authenticated:
            return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = PostCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세보기, 수정, 삭제 뷰(get, put, delete) - get 빼고 본인만 가능
class PostDetailView(APIView):
    def get(self, request, post_id):
        '''특정 게시글 조회'''
        posts = get_object_or_404(Post, id=post_id)
        serializer = PostDetailSerializer(posts)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, post_id):
        '''게시글 수정'''
        posts = get_object_or_404(Post, id=post_id)
        if request.user == posts.owner:
            serializer = PostCreateSerializer(posts, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("작성자만 수정할 수 있습니다.", status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, post_id):
        '''게시글 삭제'''
        posts = get_object_or_404(Post, id=post_id)
        if request.user == posts.owner:
            posts.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("작성자만 삭제할 수 있습니다.", status=status.HTTP_403_FORBIDDEN)
