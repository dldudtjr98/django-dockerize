from django.urls import path
from rest_framework import renderers
from .views import UserReadViewSet, UserViewSet
from . import views


user_list = UserReadViewSet.as_view({
    'get': 'list'
})
user_detail = UserReadViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('user_all/', user_list, name='user-list'),
    path('user_detail/<int:pk>/', user_detail, name='user-detail'),
    path('user_add/', views.UserView.as_view()),
    path('user_modify/<int:pk>/', views.UserView.as_view()),
    path('user_delete/<int:pk>/', views.UserView.as_view()),
]

