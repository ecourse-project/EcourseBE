from django.db.models import Prefetch

from apps.posts.models import Post


class PostsService:
    @property
    def get_all_posts_queryset(self):
        return Post.objects.prefetch_related("images").select_related("thumbnail", "topic")

    def get_posts_by_topic(self, topic):
        if topic.strip():
            return self.get_all_posts_queryset.filter(topic__name__icontains=topic.strip())
        return Post.objects.none()