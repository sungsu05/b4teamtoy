from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from posts.models import Post
from comments.models import Comment
from comments.serializers import CommentSerializer,CommentCreateSerializer
from rest_framework.generics import get_object_or_404






# @@@@@@@@@@@@@@@@댓글@@@@@@@@@@@@@@@@
class CommentView(APIView):
    def get(self, request, post_id):
        posts = Post.objects.get(id=post_id)
        comments = posts.comment_set.all() 
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        serializer = CommentCreateSerializer(data=request.data, context={"owner": request.user, "posts_id": post_id})
        if serializer.is_valid():
            serializer.save(owner=request.user, posts_id=post_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#@@@@@@@@@@@@@@@@댓글 수정@@@@@@@@@@@@@@@@ 
class CommentDetailView(APIView):
    def put(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.owner:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)
   





    # @@@@@@@@@@@@@@@@댓글 삭제@@@@@@@@@@@@@@@@  
    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.owner:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)

