
from threading import Lock
import base64
from PIL import Image
from io import BytesIO
import numpy as np
from events import deboog

# to show image in browser
from js import document, window, Uint8Array, File

class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class Game():
    __metaclass__ = SingletonMeta
    
    def __init__(self) -> None:
        self.frame_count = 0
    
    def save_frame(self, frame):
    #  pasar de base64 a pillow Image
        imgdata = base64.b64decode(frame.split(',')[-1])
        # img = skimage.io.imread(imgdata, plugin='imageio')
        img = Image.open(BytesIO(imgdata))
        processed = img.convert('L').resize((round(img.width/8), round(img.height / 8)))
        array = np.asarray(processed)


        # # # pasar de Image a base64
        # SAVE THE IMAGE:
        buf = BytesIO()
        processed.save(buf, format='PNG')
        # SHOW IMG IN BROWSER:
        # Image.fromarray(skimage.img_as_ubyte(img)).save(buf, format='PNG')
        image_file = File.new([Uint8Array.new(buf.getvalue())], "new_image_file.png", {type: "image/png"})
        document.getElementById('ca').src = window.URL.createObjectURL(image_file)
    