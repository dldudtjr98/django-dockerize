from django.urls import path
from .views import CurriculumView


urlpatterns = [
    path('curriculum', CurriculumView.as_view()),
    path('curriculum/<int:pk>', CurriculumView.as_view())
]
