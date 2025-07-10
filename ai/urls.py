from django.urls import path
from .views import CareerQuestionnaireApiView, LogListApiView

urlpatterns = [
    path('questionnaire/', view=CareerQuestionnaireApiView.as_view(), name='career_api'),
    path('logs/', view=LogListApiView.as_view(), name='questionaire_log')
]
