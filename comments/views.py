# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
# from comments.models import Comment
# from posts.models import Post

# # 댓글
# class CommentView(APIView):
# 	def get(self, request, post_id):
# 		posts = Post.objects.get(id=post_id)
#         comments = posts.comment_set.all()
#         serializer = CommentSerializer(comments,many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
  	
#     def post(self, request, post_id):
#         pass
    	   

# 댓글 수정 삭제
# class CommnentDetailView(APIView):
# 	def put(self, request, post_id):
# 		pass
    	 
#     def del(self, request, post_id):
#         pass

# posts id를 몰라서 틀만 잡고 하는중이였습니다!    	   