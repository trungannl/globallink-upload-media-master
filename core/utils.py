import json
from PIL import Image

def getBody(requests):
    body_unicode = requests.body.decode('utf-8')
    try:
        variables = json.loads(body_unicode)
        return variables
    except:
        return None

def convertToWebp(imageSource, imageName="Undefined.webp"):
    """Convert image to webp image

    Args:
        imageSource (ImageSource): The image source
        imageName (str, optional): The image name. Defaults to "Undefined.webp".

    Returns:
        str: The webp image name
    """
    extension = imageName.split(".")[-1]
    imageName = imageName.replace(extension, "webp")
    image = Image.open(imageSource)
    image = image.convert("RGB")
    image.save(imageName, "webp")
    return imageName

