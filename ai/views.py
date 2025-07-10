from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionaireSubmissionSerializer, QuestionSerializer
from .models import CareerQuizSubmissionModel
from lib.quiz import QuizClass
import json

# Create your views here.


class CareerQuestionnaireApiView(APIView):
    def get(self, request):
        serializer = QuestionSerializer({
            "id": 1,
            "question": "Where are you in your professional development?",
            "options": [
                "student",
                "early-career professional",
                "late career professional",
                "lifelong learner"
            ],
            "multiple_answers": False
        })
        return Response(data=serializer.data, status=status.HTTP_200_OK)

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

            # If the response includes a list of recommendations and reasoning
            if "career_recommendations" in response and "reasoning" in response:
                CareerQuizSubmissionModel.objects.create(
                    questions=career_quiz,
                    answers=user_response,
                    recommendations=response["career_recommendations"],
                    reasoning=response["reasoning"]
                )

            return Response({
                "message": "Submission received",
                "data": response,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
