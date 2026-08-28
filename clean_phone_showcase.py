from pathlib import Path
from PIL import Image
from rembg import remove, new_session

source = Path('/home/ubuntu/mostaplace-work/phone-showcase-transparent-final.png')
target = Path('/home/ubuntu/mostaplace-work/app/frontend_test_copy/client/public/phones-icons/phones-accessories-showcase-transparent.webp')
target.parent.mkdir(parents=True, exist_ok=True)
with Image.open(source).convert('RGB') as image:
    cutout = remove(image, session=new_session('u2net'), alpha_matting=False).convert('RGBA')
    alpha = cutout.getchannel('A').point(lambda value: 0 if value < 8 else value)
    cutout.putalpha(alpha)
    cutout.save(target, 'WEBP', lossless=True, method=6)
    print(f'{target} {cutout.width}x{cutout.height} {target.stat().st_size} bytes')
