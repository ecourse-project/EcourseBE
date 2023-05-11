course = [
  {
    "name": "Test script",
    "topic": "test script",
    "description": "test script",
    "price": 19000000,
    "lessons": [
        {
            "name": "Bai 1",
            "lesson_number": 1,
            "content": "Bai 1",
            "documents": [
                {
                    "name": "Doc bai 1",
                    "description": "Doc bai 1",
                    "topic": "test 1",
                }
            ]
        },
        {
            "name": "Bai 2",
            "lesson_number": 2,
            "content": "Bai 2",
            "documents": [
                {
                    "name": "Doc bai 2",
                    "description": "Doc bai 2",
                    "topic": "test 2"
                }
            ]
        }
    ]
  }
]


from apps.courses.models import Course, CourseDocument, Lesson, CourseTopic



class UploadCourseServices:
    def create_course_data(self, courses: list):
        courses_lessons = [self.prepare_course_data(course) for course in courses]
        course_objects = Course.objects.bulk_create([course[0] for course in courses_lessons])

        for index, obj in enumerate(course_objects):
            if courses_lessons[index][1]:
                obj.lessons.add(*courses_lessons[index][1])

        return course_objects

    def prepare_course_data(self, course: dict):
        course_topic = None
        if course.get("topic"):
            course_topic, created = CourseTopic.objects.get_or_create(name=course.pop("topic"))
        if course.get("lessons"):
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
        if lesson.get("documents"):
            documents = lesson.pop("documents")
            return Lesson(**lesson), self.create_document_data(documents)
        return Lesson(**lesson), None

    def create_document_data(self, documents: list) -> list:
        return CourseDocument.objects.bulk_create(
            [self.prepare_document_data(doc) for doc in documents]
        )

    def prepare_document_data(self, document: dict):
        document_topic = None
        if document.get("topic"):
            document_topic, created = CourseTopic.objects.get_or_create(name=document.pop("topic"))
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





