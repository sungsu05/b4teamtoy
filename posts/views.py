from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from posts.models import Post
from posts.serializers import PostlistSerializer, PostCreateSerializer, PostDetailSerializer, MyPostSerializer 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
        # is_seller추가 
        if not request.user.is_seller:
            return Response("판매자만 글 작성이 가능합니다.", status=status.HTTP_401_UNAUTHORIZED)
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
        if request.user == posts.owner: # 아마 유저인증과정ㅇ ㅓㅄ어도 토큰만으로 될 수도 있는지? 아닌지. 호기심! 
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
        
class LikeView(APIView):
    def post(self, request, post_id):
        posts = get_object_or_404(Post, id=post_id)
        # 로그인 인증 추가
        if not request.user.is_authenticated:
            return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED)
        else:
            if request.user in posts.likes.all():
                posts.likes.remove(request.user)
                return Response("좋아요를 취소했습니다.", status=status.HTTP_200_OK)
            else:
                posts.likes.add(request.user)
                return Response("좋아요를 했습니다.", status=status.HTTP_200_OK)


class MyPostListView(APIView):
    def get(self, request, user_id):
        '''내 게시글만 모아보기'''
        posts = Post.objects.filter(owner_id=user_id)
        serializer = MyPostSerializer (posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # if ~~~
        # else:
        #     return Response("자신의 페이지만 볼 수 있습니다.", status=status.HTTP_403_FORBIDDEN)
        # 본인이 아니면 페이지에 접근못하게 하고 싶은데 잘안되네요!!