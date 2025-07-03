from django.urls import path
from .views import HelloWorldView, HelloNameView

urlpatterns = [
    path('hello/', view=HelloWorldView.as_view(), name='hello-world'),
    path('hello/<str:name>', view=HelloNameView.as_view(), name='hello-name')
]
