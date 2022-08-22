from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser,JSONParser
from rest_framework import status
from rest_framework.response import Response
from .cron import download_image, create_thumb_s3
from core.utils import getBody
import logging
from drf_yasg.utils import swagger_auto_schema
from core.models import  ResponseModelSerializer, ResponseSuccessModelSerializer
from .serializers import UrlRequestSerializer
logger = logging.Logger(__name__)


@swagger_auto_schema(tags=["Upload image to s3 from url"], methods=['POST'], operation_description="Upload webp image to s3 from url",
                     responses={400: ResponseModelSerializer,
                                200: ResponseSuccessModelSerializer},
                     request_body=UrlRequestSerializer, operation_id="upload_image_from_url")
@api_view(["POST"])
@parser_classes([MultiPartParser, JSONParser])
def postImage(requests):
    headers = {
        "Access-Control-Allow-Origin": "*"
    }
    
    try:
        url = requests.POST.get("url")
        if url is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        fileName = download_image(url)
        if fileName is not None:
            create_thumb_s3(fileName)
        return Response(status=status.HTTP_200_OK, headers=headers)
    except Exception as e:
        logger.error(e)
        response = ResponseModelSerializer(
                {"message": "Upload was fail."})
        return Response(response, status=400, headers=headers)
