from django.urls import path
from .views import CurriculumView


urlpatterns = [
    path('curriculum', CurriculumView.as_view(), name='curriculum_without_pk'),
    path('curriculum/<int:pk>', CurriculumView.as_view(), name='curriculum_with_pk')
]
