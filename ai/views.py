from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HelloSerializer, QuestionaireSubmissionSerializer
from lib.quiz import QuizClass
import json

# Create your views here.


class HelloWorldView(APIView):
    def get(self, request):
        data = {"message": "Hello World"}
        serializer = HelloSerializer(data)
        return Response(serializer.data)


class HelloNameView(APIView):
    def get(self, request, name):
        message = f"Hello {name}!"
        serializer = HelloSerializer({'message': message})
        return Response(serializer.data)


class CareerQuestionaireApiView(APIView):
    def post(self, request):
        serializer = QuestionaireSubmissionSerializer(data=request.data)
        quiz = QuizClass()
        if serializer.is_valid():
            career_quiz = serializer.validated_data['questions']
            user_response = serializer.validated_data['answers']

            user_prompt_template, system_prompt_template = quiz.load_prompts()
            user_prompt, system_prompt = quiz.format_prompts(
                user_prompt_template, system_prompt_template, career_quiz, user_response)

            raw_responze = quiz.llm(
                user_prompt=user_prompt, system_prompt=system_prompt)
            response = json.loads(raw_responze)

            return Response({
                "message": "Submission received",
                "data": response,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
