from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.core.pagination import StandardResultsSetPagination
from apps.posts.api.serializers import PostSerializer
from apps.posts.services.services import PostsService


class PostListView(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get_queryset(self):
        if self.request.query_params.get("topic"):
            return PostsService().get_posts_by_topic(self.request.query_params.get("topic"))
        return PostsService().get_all_posts_queryset


class PostRetrieveView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get_object(self):
        return PostsService().get_all_posts_queryset.filter(id=self.request.query_params.get("post_id")).first()

