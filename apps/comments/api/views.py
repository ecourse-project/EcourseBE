from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.comments.models import Comment, ReplyComment
from apps.comments.api.serializers import CommentSerializer
from apps.comments.services import get_comments_queryset


class CreateCommentView(APIView):
    def post(self, request, *args, **kwargs):
        comment_data = self.request.data
        if comment_data.get("owner_id") is None:
            comment = Comment.objects.create(
                content=comment_data.get("content"),
                user_id=comment_data.get("user_id"),
                course_id=comment_data.get("course_id"),
            )
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

        comment = Comment.objects.get(id=comment_data.get("owner_id"))
        comment.reply_comments.add(
            ReplyComment.objects.create(
                user_id=comment_data.get("user_id"),
                content=comment_data.get("content"),
            )
        )
        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)


class ListAllCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return get_comments_queryset().filter(course_id=self.request.query_params.get("course_id"))
