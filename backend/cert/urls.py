from django.urls import path
from .views import UserView, GroupView


urlpatterns = [
    path('member', UserView.as_view(), name='member_without_pk'),
    path('member/<int:pk>', UserView.as_view(), name='member_with_pk'),
    path('group', GroupView.as_view(), name='group_without_pk'),
    path('group/<int:pk>', GroupView.as_view(), name='group_with_pk'),
]
