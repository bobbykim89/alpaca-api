from rest_framework import serializers


class HelloSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField()
    selections = serializers.ListField(child=serializers.CharField())


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField())
    multiple_answers = serializers.BooleanField()


class QuestionaireSubmissionSerializer(serializers.Serializer):
    questions = QuestionSerializer(many=True)
    answers = AnswerSerializer(many=True)
