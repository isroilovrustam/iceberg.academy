from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseAPI.as_view()),
    path('<int:pk>/', views.CourseDetailAPI.as_view()),
    path('task/<int:pk>/', views.TaskDetailAPI.as_view()),
    path('task-answer/', views.AnswerTaskAPI.as_view()),
]