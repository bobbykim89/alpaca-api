from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionaireSubmissionSerializer, QuestionSerializer, QuestionnaireLogModelSerializer, CareerRecommendationsRequestSerializer, CareerRecommendationsLogModelSerializer
from .models import CareerQuizSubmissionModel, DegreeRecommendationSubmissionModel
from lib.quiz import QuizClass
from lib.degree_recommendation import DegreeRecommendation
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


class CareerQuestionnaireLogListApiView(ListAPIView):
    serializer_class = QuestionnaireLogModelSerializer
    queryset = CareerQuizSubmissionModel.objects.all()


class DegreeRecommendationApiView(APIView):
    def get(self, request):
        data = {
            "selected_career": "selected career from quiz",
            "answers": ["answers from quiz"]
        }
        return Response({
            "message": "This route only support POST method.",
            "data": data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CareerRecommendationsRequestSerializer(data=request.data)
        degree_recommendation = DegreeRecommendation()
        if serializer.is_valid():
            # obtain user quiz answers and career selection (only 1)
            career_selected = serializer.validated_data['selected_career']
            quiz_answers = serializer.validated_data['answers']

            # generate user profile
            user_profile = degree_recommendation.generate_user_profile(
                quiz_answers=quiz_answers)

            # get top 5 hits for degrees
            hits = degree_recommendation.search(
                selected_career=career_selected, user_profile=user_profile, limit=5)

            # format data
            recommended_degrees = degree_recommendation.format_hits_response(
                hits=hits)

            user_prompt, system_prompt = degree_recommendation.format_prompt(
                career=career_selected, career_quiz=user_profile, degrees=recommended_degrees)
            raw_response = degree_recommendation.llm(
                user_prompt=user_prompt, system_prompt=system_prompt)
            response = json.loads(raw_response)

            DegreeRecommendationSubmissionModel.objects.create(
                selected_career=career_selected,
                answers=user_profile,
                recommendations=response,
            )

            return Response({
                "message": "Submission received",
                "data": response,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationLogsListApiView(ListAPIView):
    serializer_class = CareerRecommendationsLogModelSerializer
    queryset = DegreeRecommendationSubmissionModel.objects.all()
