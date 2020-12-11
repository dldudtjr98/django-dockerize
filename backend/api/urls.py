from django.urls import path
from api.views import ArticleList


urlpatterns = [
    path('articles/', ArticleList.as_view(), name='articles'),
]

