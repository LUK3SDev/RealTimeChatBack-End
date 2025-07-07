from django.urls import path
from .api.view import (
    RegisterView, LoginView, 
    SetPublicKeyUser, GetPublicKeyUser,
    InfoUser, ListUsers
)



urlpatterns = [
    path('account/register/', RegisterView.as_view()),
    path('account/login/', LoginView.as_view()),
    path('account/set_public_key/', SetPublicKeyUser.as_view()),
    path('account/get_public_key/', GetPublicKeyUser.as_view()),
    path('account/user/', InfoUser.as_view()),
    path('account/users/', ListUsers.as_view()),
]
