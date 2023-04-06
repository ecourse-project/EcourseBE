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

import os
from uuid import uuid4
from math import ceil

from django.core.files.storage import default_storage

from apps.upload.services.storage.base import get_file_path
from apps.upload.models import UploadImage, UploadFile
from apps.courses.models import CourseDocument, Lesson



class UploadCourseServices:
    def prepare_course_data(self, course_data: dict):
        if course_data.get("lessons"):
            lessons = course_data.pop("lessons")



    def create_lesson_data(self, lessons: list):
        for lesson in lessons:
            videos = None
            documents = None



    def prepare_lesson_data(self, lesson: dict):
        documents = None
        if lesson.get("documents"):
            documents = lesson.pop("documents")




    def create_document_data(self, documents: list):
        return CourseDocument.objects.bulk_create(
            [self.prepare_document_data(doc) for doc in documents]
        )

    def prepare_document_data(self, document: dict):
        return CourseDocument(**document)

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





