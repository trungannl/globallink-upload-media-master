import os
import requests
import shutil
import boto3
from PIL import Image
import urllib.request

access_key_src = os.environ.get("AWS_ACCESS_KEY_ID")
secret_key_src = os.environ.get("AWS_SECRET_ACCESS_KEY")
region_name = os.environ.get("AWS_REGION_NAME")
bucket_name = os.environ.get("AWS_MEDIA_BUCKET_NAME")
bucket_folder = os.environ.get("AWS_BUCKET_BASE_FOLDER","")

def convert_image_name(old_name, append_name):
    names = old_name.split(".")
    extension = names[1]
    new_name = names[0] + "-" + append_name + "." + extension
    return new_name


def create_thumb_s3(image_file):
    s3 = boto3.resource('s3', region_name=region_name,
                        aws_access_key_id=access_key_src,
                        aws_secret_access_key=secret_key_src)
    bucket = s3.Bucket(bucket_name)

    if not os.path.exists("__sized__/products"):
        os.makedirs("__sized__/products")

    keys = {
        "products": [
            ("product_gallery", "thumbnail__540x540"),
            ("product_gallery_2x", "thumbnail__1080x1080"),
            ("product_small", "thumbnail__60x60"),
            ("product_small_2x", "thumbnail__120x120"),
            ("product_list", "thumbnail__255x255"),
            ("product_list_2x", "thumbnail__510x510"),
        ]
    }
    for output in keys['products']:
        values = output[1].split("__")
        if len(values) != 2:
            return
        output_size_str = values[1].split("x")
        output_size = tuple(list(map(int, output_size_str)))

        img = Image.open(image_file)

        img.thumbnail(output_size)
        image_path_thumb = convert_image_name(
            image_file.replace("images", "__sized__/products"),
            values[0] + "-" + values[1])

        img.save(image_path_thumb)

        new_image_name = bucket_folder+image_path_thumb.replace(
            "app/media/", "")

        bucket.upload_file(image_path_thumb, new_image_name,
                           ExtraArgs={"ContentType": "image/webp"})

        os.remove(image_path_thumb)

    os.remove(image_file)

    pass

    """download image from url
    """


def download_image(url):
    fileName = url.split("/")[-1]
    fileName = os.path.join("images", fileName)
    path = os.path.dirname(fileName)
    if not os.path.exists(path):
        os.makedirs(path)
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'Upload media service')
    fileName, headers = opener.retrieve(url, fileName)
    # fileName = opener.retrieve(url, fileName)
    return fileName
