
import datetime
import time
from PIL import Image
import BytesIO
import base64

start_time = time.time()

def get_uptime():
    return '{}'.format(datetime.timedelta(seconds=time.time() - start_time))


def decode_image(images):
    if isinstance(images, list):
        images = []
        for image in images:
            img = Image.open(BytesIO(base64.b64decode(images)))
            img = img.convert('RGB')
            images.append(img)
        return images

    elif isinstance(images, str):
        img = Image.open(BytesIO(base64.b64decode(images)))
        img = img.convert('RGB')
        return img
    else:
        return images
