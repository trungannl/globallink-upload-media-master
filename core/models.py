from rest_framework import serializers


class ResponseModelSerializer(serializers.Serializer):
    error = serializers.BooleanField(default=True)
    message = serializers.CharField(max_length=255, default="")


class ResponseSuccessModelSerializer(ResponseModelSerializer):
    url = serializers.URLField()


class RequestSerializer(serializers.Serializer):
    prefix = serializers.CharField(max_length=255, required=False)
    bucket_name = serializers.CharField(
        max_length=255, required=True)
    image = serializers.ImageField(required=True)
