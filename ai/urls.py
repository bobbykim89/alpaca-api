from django.urls import path
from .views import CareerQuestionnaireApiView

urlpatterns = [
    path('questionnaire/', view=CareerQuestionnaireApiView.as_view(), name='career_api')
]
