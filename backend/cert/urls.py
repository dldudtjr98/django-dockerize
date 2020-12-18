from django.urls import path
from .views import UserView, GroupView


urlpatterns = [
    path('member', UserView.as_view()),
    path('member/<int:pk>', UserView.as_view(), name='member_rest_api'),
    path('group', GroupView.as_view()),
    path('group/<int:pk>', GroupView.as_view()),
]
