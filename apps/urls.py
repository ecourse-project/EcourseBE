from django.urls import path, include

urlpatterns = [
    path("users-auth/", include("apps.users_auth.api.urls")),
    path("users/", include("apps.users.api.urls")),
    path("upload/", include("apps.upload.api.urls")),
    path("documents/", include("apps.documents.api.urls")),
    path("courses/", include("apps.courses.api.urls")),
    path("classes/", include("apps.classes.api.urls")),
    path("carts/", include("apps.carts.api.urls")),
    path("payment/", include("apps.payment.api.urls")),
    path("comments/", include("apps.comments.api.urls")),
    path("quiz/", include("apps.quiz.api.urls")),
    path("rating/", include("apps.rating.api.urls")),
    path("settings/", include("apps.settings.api.urls")),
    path("posts/", include("apps.posts.api.urls")),
    path("configuration/", include("apps.configuration.api.urls")),
    path("system/", include("apps.system.api.urls")),
]
