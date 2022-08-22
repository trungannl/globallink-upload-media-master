from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

urlpatterns = [
    url(
        r'^api/images/upload/$',
        views.uploadImage,
        name='image upload'
    ),
]
