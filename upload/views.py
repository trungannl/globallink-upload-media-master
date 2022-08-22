from rest_framework.decorators import api_view, action, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import boto3
import os
from PIL import Image
from core.models import RequestSerializer, ResponseModelSerializer, ResponseSuccessModelSerializer
from drf_yasg.utils import swagger_auto_schema
access_key_src = os.environ.get("AWS_ACCESS_KEY_ID")
secret_key_src = os.environ.get("AWS_SECRET_ACCESS_KEY")
region_name = os.environ.get("AWS_REGION_NAME")
bucket_name = os.environ.get("AWS_MEDIA_BUCKET_NAME")
base_folder = os.environ.get("AWS_BUCKET_BASE_FOLDER")
protocol = os.environ.get("PROTOCOL")
DIRECTION = "__uploads__"

import logging
logger = logging.Logger(__name__)

@swagger_auto_schema(tags=["Upload image to s3"], methods=['POST'], operation_description="Upload image to s3",
                     responses={400: ResponseModelSerializer,
                                200: ResponseSuccessModelSerializer},
                     request_body=RequestSerializer, operation_id="upload_image")
@api_view(["POST"])
@parser_classes([MultiPartParser,])
def uploadImage(requests):
    headers = {
        "Access-Control-Allow-Origin": "*"
    }
    
    s3 = boto3.resource('s3', region_name=region_name,
                        aws_access_key_id=access_key_src,
                        aws_secret_access_key=secret_key_src)
    # bucket_name = requests.POST.get("bucket_name")
    bucket = s3.Bucket(bucket_name)

    try:
        direction = ""
        prefix = requests.POST.get('prefix')
        if prefix:
            direction = str(requests.data["prefix"]) + "/"

        data = requests.data["image"]
        img = Image.open(data)
        content_type = data.content_type

        if direction and not os.path.exists(direction):
            os.makedirs(direction)

        data = requests.data["image"]
        img = Image.open(data)
        file_name = data.name
        img.save(direction + file_name)
        bucket.upload_file(direction + file_name, direction + file_name,
                           ExtraArgs={"ContentType": content_type,
                                      'ACL': 'public-read'})
        os.remove(direction + file_name)
        if direction:
            os.rmdir(direction)

        data = {
            "error": "False",
            "data": "https://" + bucket_name + ".s3.amazonaws.com/" + direction + file_name
        }
        return Response(data, status=200, headers=headers)
    except Exception as ex:
        logger.error(ex)
        response = {"message": "Upload was fail."}
        return Response(response, status=400, headers=headers)