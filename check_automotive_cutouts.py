from pathlib import Path
from PIL import Image

folder = Path('/home/ubuntu/mostaplace-work/app/frontend_test_copy/client/public/automotive-icons/cutouts')
for path in sorted(folder.glob('*.webp')):
    with Image.open(path) as image:
        alpha = image.getchannel('A')
        bbox = alpha.getbbox()
        print(path.name, 'bbox=', bbox, 'subject=', (bbox[2]-bbox[0], bbox[3]-bbox[1]) if bbox else None, 'bytes=', path.stat().st_size)
