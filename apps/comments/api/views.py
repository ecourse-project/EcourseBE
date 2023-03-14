from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.comments.models import Comment, ReplyComment
from apps.comments.api.serializers import CommentSerializer
from apps.comments.services import get_comments_queryset
from apps.comments.exceptions import CheckContentLengthException
from apps.core.pagination import StandardResultsSetPagination


class CreateCommentView(APIView):
    def post(self, request, *args, **kwargs):
        comment_data = self.request.data
        content = comment_data.get("content")
        user_id = comment_data.get("user_id")
        if content == "" or len(content) > 500:
            raise CheckContentLengthException

        if not comment_data.get("owner_id"):
            comment = Comment.objects.create(
                content=content,
                user_id=user_id,
                course_id=comment_data.get("course_id"),
            )
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

        comment = Comment.objects.get(id=comment_data.get("owner_id"))
        comment.reply_comments.add(
            ReplyComment.objects.create(
                user_id=user_id,
                content=content,
            )
        )
        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)


class ListAllCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return get_comments_queryset().filter(course_id=self.request.query_params.get("course_id")).order_by('-created')
