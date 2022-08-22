from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'upload-webp/', views.postImage, name='upload webp'),
    # url(r'^api/upload-webp/', views.postImage, name='upload webp'),
]