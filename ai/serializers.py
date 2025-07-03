from rest_framework import serializers


class HelloSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)
