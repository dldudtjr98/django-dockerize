from django.urls import path
from rest_framework import renderers
from .views import UserView, GroupView, UserGroupView


urlpatterns = [
    path('member', UserView.as_view()),
    path('member/<int:pk>', UserView.as_view()),
    path('group', GroupView.as_view()),
    path('group/<int:pk>', GroupView.as_view()),
    path('group/member', UserGroupView.as_view()),
]