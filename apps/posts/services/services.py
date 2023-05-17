from django.db.models import Q

from apps.posts.models import Post


class PostsService:
    @property
    def get_all_posts_queryset(self):
        return Post.objects.select_related("thumbnail", "topic")

    def get_posts_by_topic(self, topic, header=""):
        if not (topic and header):
            return Post.objects.none()

        query = Q()
        if topic.strip():
            query &= Q(topic__name__icontains=topic.strip())
        if header:
            query &= Q(header__icontains=header)
        return self.get_all_posts_queryset.filter(query)

    def get_posts_by_list_id(self, list_id, header=""):
        if not (list_id and header):
            return Post.objects.none()

        query = Q()
        if list_id:
            query &= Q(id__in=list_id)
        if header:
            query &= Q(header__icontains=header)
        return self.get_all_posts_queryset.filter(query)
