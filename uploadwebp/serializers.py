from rest_framework import serializers
class UrlRequestSerializer(serializers.Serializer):
    url = serializers.URLField()