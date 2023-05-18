from apps.carts.models import *
from apps.classes.models import *
from apps.configuration.models import *
from apps.courses.models import *
from apps.documents.models import *
from apps.payment.models import *
from apps.posts.models import *
from apps.quiz.models import *
from apps.rating.models import *
from apps.settings.models import *
from apps.upload.models import *
from apps.users.models import *


models = {
    "Cart": Cart,
    "FavoriteList": FavoriteList,
    "Class": Class,
    "ClassRequest": ClassRequest,
    "ClassManagement": ClassManagement,
    "Configuration": Configuration,
    "PersonalInfo": PersonalInfo,
    "CourseTopic": CourseTopic,
    "CourseDocument": CourseDocument,
    "Lesson": Lesson,
    "Course": Course,
    "CourseManagement": CourseManagement,
    "LessonManagement": LessonManagement,
    "CourseDocumentManagement": CourseDocumentManagement,
    "VideoManagement": VideoManagement,
    "DocumentTopic": DocumentTopic,
    "Document": Document,
    "DocumentManagement": DocumentManagement,
    "Order": Order,
    "PostTopic": PostTopic,
    "Post": Post,
    "AnswerChoices": AnswerChoices,
    "Quiz": Quiz,
    "Answer": Answer,
    "Rating": Rating,
    "DocumentRating": DocumentRating,
    "CourseRating": CourseRating,
    "Header": Header,
    "HeaderDetail": HeaderDetail,
    "HomePageDetail": HomePageDetail,
    "UploadFile": UploadFile,
    "UploadImage": UploadImage,
    "UploadVideo": UploadVideo,
    "UploadCourse": UploadCourse,
    "UploadDocument": UploadDocument,
    "User": User,
    "UserResetPassword": UserResetPassword,
}