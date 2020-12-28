from django.urls import path
from .views import UserView, GroupView, UserLoginView, UserRegisterView


"""
member/logout/
POST with Header Authorization : "Token {token}" allows logout user
"""

urlpatterns = [
    path('member', UserView.as_view(), name='member_without_pk'),
    path('member/login', UserLoginView.as_view(), name='member_login'),
    path('member/register', UserRegisterView.as_view(), name='member_register'),
    path('member/<int:pk>', UserView.as_view(), name='member_with_pk'),
    path('group', GroupView.as_view(), name='group_without_pk'),
    path('group/<int:pk>', GroupView.as_view(), name='group_with_pk'),
]
