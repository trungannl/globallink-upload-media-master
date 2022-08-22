from django.conf.urls import url    
from .views import ImageUploadView

urlpatterns = [
    url(
        r'^api/image-to-webp/upload/$',
        ImageUploadView.as_view(),
        name='image upload'
    ),
]
