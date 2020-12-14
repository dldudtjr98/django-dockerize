from django.urls import path
from rest_framework import renderers
from .views import UserReadViewSet, UserView

user_list = UserReadViewSet.as_view({
    'get': 'list'
})
user_detail = UserReadViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('info/', user_list, name='user-list'),
    path('info/<int:pk>/', user_detail, name='user-detail'),
    path('add', UserView.as_view()),
    path('modify/<int:pk>', UserView.as_view()),
]