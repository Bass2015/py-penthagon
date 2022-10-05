
import base64
import numpy as np
from threading import Lock
from PIL import Image
from io import BytesIO
from collections import deque

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
    STACK_SIZE=4

    def __init__(self) -> None:
        self.frame_count = 0
        self.is_new_game = True
    
    def save_frame(self, frame):
        processed = process_frame(frame)
        if self.is_new_game:
            self.frames_stack = deque([np.zeros(processed.size, dtype=np.int) for i in range(Game.STACK_SIZE)],
                                     maxlen=Game.STACK_SIZE)
            for i in range(Game.STACK_SIZE):
                self.frames_stack.append(processed)
        else:
            self.frames_stack.append(processed)
            self.is_new_game = False
        self.state = np.stack(self.frames_stack, axis=2)


def process_frame(frame):
    #  pasar de base64 a pillow Image
    imgdata = base64.b64decode(frame.split(',')[-1])
    # img = skimage.io.imread(imgdata, plugin='imageio')
    img = Image.open(BytesIO(imgdata))
    processed = img.convert('L').resize((round(img.width/8), round(img.height / 8)))
    # show_image(processed)
    array = np.asarray(processed)/255
    return array


def show_image(image):
    # # pasar de Image a base64
    # SAVE THE IMAGE:
    buf = BytesIO()
    image.save(buf, format='PNG')
    # SHOW IMG IN BROWSER:
    # Image.fromarray(skimage.img_as_ubyte(img)).save(buf, format='PNG')
    image_file = File.new([Uint8Array.new(buf.getvalue())], "new_image_file.png", {type: "image/png"})
    document.getElementById('ca').src = window.URL.createObjectURL(image_file)

   
        