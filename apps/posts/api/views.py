from django.db.models import F

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.core.pagination import StandardResultsSetPagination
from apps.posts.api.serializers import PostSerializer, ListPostSerializer
from apps.posts.services.services import PostsService
from apps.posts.models import PostTopic


class PostListView(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = ListPostSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get_queryset(self):
        topic = self.request.query_params.get("topic", "").strip()
        list_id = self.request.query_params.getlist('course_id')
        if topic:
            return PostsService().get_posts_by_topic(topic)
        elif list_id:
            return PostsService().get_posts_by_list_id(list_id)
        else:
            return PostsService().get_all_posts_queryset


class PostRetrieveView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get_object(self):
        return PostsService().get_all_posts_queryset.filter(id=self.request.query_params.get("post_id")).first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = F("views") + 1
        instance.save(update_fields=["views"])
        return super(PostRetrieveView, self).retrieve(self, request, *args, **kwargs)


class PostTopicListView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        return Response(data=list(PostTopic.objects.all().values_list("name", flat=True)))

