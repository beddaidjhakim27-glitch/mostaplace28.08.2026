from pathlib import Path
from PIL import Image

source = Path('/home/ubuntu/upload/pasted_file_i5IVzz_ChatGPTImage22août2026,17_54_41.png')
with Image.open(source) as image:
    print('name=', source.name)
    print('size=', image.size)
    print('mode=', image.mode)

for module_name in ('rembg', 'cv2', 'numpy'):
    try:
        __import__(module_name)
        print(module_name, '=available')
    except Exception as exc:
        print(module_name, '=unavailable', type(exc).__name__)
