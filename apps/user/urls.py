from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserAPIView.as_view()),
    path("team/", views.TeamAPIView.as_view()),
    path("team/<int:pk>/", views.TeamDetailAPI.as_view()),
    path("register/", views.RegisterAPIView.as_view()),
    path("verify-phone/", views.VerifyPhoneAPI.as_view()),
    path("change-password/", views.ChangePasswordAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("forget-password/", views.ForgetPasswordAPIView.as_view()),
    path("forget-password-verify/", views.VerifyCodeAPIView.as_view()),
    path("forget-password-confirm/", views.ForgetPasswordConfirmAPIView.as_view()),
]
