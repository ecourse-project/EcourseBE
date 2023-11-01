# from celery import Celery
# import os
# from django.conf import settings
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecourse.settings')
# app = Celery('ecourse')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
