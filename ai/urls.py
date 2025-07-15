from django.urls import path
from .views import CareerQuestionnaireApiView, CareerQuestionnaireLogListApiView, DegreeRecommendationApiView, RecommendationLogsListApiView

urlpatterns = [
    path('questionnaire/', view=CareerQuestionnaireApiView.as_view(), name='career_api'),
    path('questionnaire/logs/', view=CareerQuestionnaireLogListApiView.as_view(),
         name='questionaire_log'),
    path('recommendation/', view=DegreeRecommendationApiView.as_view(),
         name='degree_recommendation'),
    path('recommendation/logs/', view=RecommendationLogsListApiView.as_view(),
         name='degree_recommendation_log')
]
