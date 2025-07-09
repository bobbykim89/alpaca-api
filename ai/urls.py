from django.urls import path
from .views import HelloWorldView, HelloNameView, CareerQuestionaireApiView

urlpatterns = [
    path('hello/', view=HelloWorldView.as_view(), name='hello-world'),
    path('hello/<str:name>/', view=HelloNameView.as_view(), name='hello-name'),
    path('questionaire/', view=CareerQuestionaireApiView.as_view(), name='career_api')
]
