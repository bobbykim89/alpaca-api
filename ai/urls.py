from django.urls import path
from .views import HelloWorldView, HelloNameView, CareerApiView

urlpatterns = [
    path('hello/', view=HelloWorldView.as_view(), name='hello-world'),
    path('hello/<str:name>/', view=HelloNameView.as_view(), name='hello-name'),
    path('career/', view=CareerApiView.as_view(), name='career_api')
]
