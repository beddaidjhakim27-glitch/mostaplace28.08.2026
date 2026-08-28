from pathlib import Path
from PIL import Image

path = Path('/home/ubuntu/mostaplace-work/app/frontend_test_copy/client/public/phones-icons/phones-accessories-showcase-transparent.webp')
image = Image.open(path).convert('RGBA')
alpha = image.getchannel('A')
transparent = sum(1 for value in alpha.getdata() if value == 0)
opaque = sum(1 for value in alpha.getdata() if value == 255)
print({"size": image.size, "mode": image.mode, "transparent_pixels": transparent, "opaque_pixels": opaque, "file_bytes": path.stat().st_size})
