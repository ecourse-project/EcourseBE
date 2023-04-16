import json
import os

from apps.courses.models import Course, CourseDocument, Lesson, CourseTopic, LessonManagement, CourseManagement
from apps.courses.services.admin import init_course_mngt, prepare_course_to_create
from apps.documents.models import Document, DocumentTopic, DocumentManagement
from apps.documents.services.admin import init_doc_mngt, prepare_doc_to_create
from apps.users.services import get_active_users


class UploadCourseServices:
    # def generate_course(self):
    #     root = "templates/data/lionel_messi/"
    #     list_files = os.listdir(root)
    #     info = json.load(open(root + "info.json", encoding="utf-8"))
    #     description = json.load(open(root + "description.json", encoding="utf-8"))
    #     list_files.remove("info.json")
    #     list_files.remove("description.json")
    #     lessons = [json.load(open(root + file, encoding="utf-8")) for file in list_files]
    #     for number, lesson in enumerate(lessons, start=1):
    #         lesson["lesson_number"] = number
    #
    #     course = dict(**info, **description)
    #     course["lessons"] = lessons
    #     UploadCourseServices().create_course_data([course])


    def create_course_data(self, courses: list):
        courses_lessons = [self.prepare_course_data(course) for course in courses]
        course_objects = Course.objects.bulk_create([tpl[0] for tpl in courses_lessons])
        users = get_active_users()

        lesson_mngt_list = []
        course_mngt_list = []
        for index, obj in enumerate(course_objects):
            if courses_lessons[index][1]:
                obj.lessons.add(*courses_lessons[index][1])
                lesson_mngt_list.extend([LessonManagement(course=obj, lesson=lesson) for lesson in courses_lessons[index][1]])
            if not obj.course_of_class:
                course_mngt_list.extend(prepare_course_to_create(course=obj, users=users))

        if lesson_mngt_list:
            LessonManagement.objects.bulk_create(lesson_mngt_list)
        if course_mngt_list:
            CourseManagement.objects.bulk_create(course_mngt_list)

        return course_objects

    def prepare_course_data(self, course: dict):
        keys = course.keys()

        if "price" in keys:
            if not course.get("price") or course.get("course_of_class"):
                course["price"] = 0

        course_topic = None
        if "topic" in keys:
            course_topic = course.pop("topic")
            if course_topic:
                course_topic = course_topic.strip().title() or None
        if course_topic:
            course_topic = (
                CourseTopic.objects.filter(name__iexact=course_topic) or
                CourseTopic.objects.create(name=course_topic)
            )

        if isinstance(course.get("lessons"), list):
            lessons = course.pop("lessons")
            return Course(**course, topic=course_topic), self.create_lesson_data(lessons)
        return Course(**course, topic=course_topic), None

    def create_lesson_data(self, lessons: list) -> list:
        lessons_docs = [self.prepare_lesson_data(lesson) for lesson in lessons]
        lesson_objects = Lesson.objects.bulk_create([lesson[0] for lesson in lessons_docs])

        for index, obj in enumerate(lesson_objects):
            if lessons_docs[index][1]:
                obj.documents.add(*lessons_docs[index][1])

        return lesson_objects

    def prepare_lesson_data(self, lesson: dict):
        if isinstance(lesson.get("documents"), list):
            documents = lesson.pop("documents")
            return Lesson(**lesson), self.create_document_data(documents)
        return Lesson(**lesson), None

    def create_document_data(self, documents: list) -> list:
        return CourseDocument.objects.bulk_create(
            [self.prepare_document_data(doc) for doc in documents]
        )

    def prepare_document_data(self, document: dict):
        document_topic = None
        if "topic" in document.keys():
            document_topic = document.pop("topic")
            if document_topic:
                document_topic = document_topic.strip().title()
        if document_topic:
            document_topic = (
                CourseTopic.objects.filter(name__iexact=document_topic).first() or
                CourseTopic.objects.create(name=document_topic)
            )
        return CourseDocument(**document, topic=document_topic)

    # def create_upload_image_data(self, image: dict):
    #     object_id = uuid4()
    #     save_path, file_ext = get_file_path(file_name=image["image_path"], new_file_name=object_id)
    #     default_storage.save(save_path, open(image["image_path"], "rb"))
    #     print(os.path.getsize("media/" + save_path))
    #     return UploadImage.objects.create(
    #         id=object_id,
    #         image_name=image.get("image_name"),
    #         image_path=save_path,
    #         image_size=os,
    #         image_type=file_ext or None,
    #     )
        # image_obj.image_size = ceil(image_obj.image_path.size / 1024)


class UploadDocumentServices:
    def create_document_data(self, documents: list):
        created_docs = Document.objects.bulk_create([self.prepare_document_data(doc) for doc in documents])
        users = get_active_users()
        list_docs = []
        for doc in created_docs:
            list_docs.extend(prepare_doc_to_create(doc, users))
        if list_docs:
            return DocumentManagement.objects.bulk_create(list_docs)
        return []

    def prepare_document_data(self, document: dict) -> Document:
        document_topic = None
        if "topic" in document.keys():
            document_topic = document.pop("topic")
            if document_topic:
                document_topic = document_topic.strip().title()
        if document_topic:
            document_topic = (
                DocumentTopic.objects.filter(name__iexact=document_topic).first() or
                DocumentTopic.objects.create(name=document_topic)
            )
        return Document(**document, topic=document_topic)
