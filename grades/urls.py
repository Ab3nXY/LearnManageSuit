# grades/urls.py
from django.urls import path
from .views import exam_grading

urlpatterns = [
    path('exam_grading/', exam_grading, name='exam_grading'),
]
