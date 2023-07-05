from django.urls import path
from .views import ContactAPIView, AboutAPIView, GoalAPIView
urlpatterns =[
    path('', ContactAPIView.as_view()),
    path('about/', AboutAPIView.as_view()),
    path('goals/', GoalAPIView.as_view()),
]