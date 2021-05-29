import cv2
import base64
import io
from PIL import Image
import numpy as np

def img_to_buff(img):
    retval, buffer = cv2.imencode('.jpg', img)
    im_buff = base64.b64encode(buffer)
    im_string = im_buff.decode('UTF-8')
    return im_string

def buf_to_img(buff):
    myfile = buff.split(',')
    imgdata = base64.b64decode(myfile[1])
    im = Image.open(io.BytesIO(imgdata))
    cv_image = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)
    return cv_image