from django.urls import path
from rest_framework import renderers
from .views import UserReadViewSet, UserView


user_list = UserReadViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('member', UserView.as_view()),
    path('member/<int:pk>', UserView.as_view()),
]