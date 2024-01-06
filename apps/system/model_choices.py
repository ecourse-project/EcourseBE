from django.contrib.auth.models import Permission, ContentType
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session

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
from apps.comments.models import *
from apps.system.models import *


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
    # "AnswerChoices": AnswerChoices,
    # "Quiz": Quiz,
    # "Answer": Answer,
    "Rating": Rating,
    "DocumentRating": DocumentRating,
    "CourseRating": CourseRating,
    "Header": Header,
    "HeaderDetail": HeaderDetail,
    "HomePageDetail": HomePageDetail,
    "UploadFile": UploadFile,
    "UploadImage": UploadImage,
    "UploadVideo": UploadVideo,
    "User": User,
    "UserResetPassword": UserResetPassword,
}


import_db_model = {
    # "contenttypes.contenttype": ContentType,
    # "auth.permission": Permission,

    "users.user": User,
    "users.userdatabackup": UserDataBackUp,
    "users.usertracking": UserTracking,
    "users.devicetracking": DeviceTracking,
    # "admin.logentry": LogEntry,

    "configuration.configuration": Configuration,
    "configuration.personalinfo": PersonalInfo,
    "users.userresetpassword": UserResetPassword,

    "upload.uploadfile": UploadFile,
    "upload.uploadvideo": UploadVideo,
    "upload.uploadfolder": UploadFolder,
    "upload.uploadimage": UploadImage,

    "documents.documenttopic": DocumentTopic,
    "documents.document": Document,
    "documents.documentmanagement": DocumentManagement,

    "courses.coursetopic": CourseTopic,
    "courses.coursedocument": CourseDocument,
    "courses.lesson": Lesson,
    "courses.course": Course,
    "courses.coursemanagement": CourseManagement,
    "courses.lessonmanagement": LessonManagement,
    "courses.coursedocumentmanagement": CourseDocumentManagement,
    "courses.videomanagement": VideoManagement,

    "classes.classrequest": ClassRequest,

    "payment.order": Order,

    "settings.header": Header,
    "settings.headerdetail": HeaderDetail,
    "settings.homepagedetail": HomePageDetail,
    "settings.category": Category,

    "posts.posttopic": PostTopic,
    "posts.post": Post,

    "carts.cart": Cart,
    "carts.favoritelist": FavoriteList,

    "comments.replycomment": ReplyComment,
    "comments.comment": Comment,

    "rating.rating": Rating,

    "sessions.session": Session,

    "system.systemconfig": SystemConfig,
    "system.storage": Storage,
    "system.visitstatistics": VisitStatistics,

    "quiz.choicename": ChoiceName,
    "quiz.choicesanswer": ChoicesAnswer,
    "quiz.choicesquestion": ChoicesQuestion,
    "quiz.matchcolumncontent": MatchColumnContent,
    "quiz.matchcolumnquestion": MatchColumnQuestion,
    "quiz.matchcolumnmatchanswer": MatchColumnMatchAnswer,
    "quiz.fillblankquestion": FillBlankQuestion,
    "quiz.questionmanagement": QuestionManagement,
    "quiz.choicesquestionuseranswer": ChoicesQuestionUserAnswer,
    "quiz.matchcolumnuseranswer": MatchColumnUserAnswer,
    "quiz.fillblankuseranswer": FillBlankUserAnswer,
    "quiz.quiz": Quiz,


    # "classes.class": Class,
    # "classes.classmanagement": ClassManagement,
    # "contenttypes.contenttype": ContentType,
    # "upload.uploadavatar": UploadImage,
    # "auth.permission": Permission,
    # "users.testuser": User,
}
