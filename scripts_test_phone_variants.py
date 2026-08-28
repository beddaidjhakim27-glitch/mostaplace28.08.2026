from pathlib import Path
from PIL import Image
from rembg import remove, new_session

source = Path('/home/ubuntu/upload/pasted_file_942F3a_ChatGPTImage22août2026,18_55_38.png')
out = Path('/home/ubuntu/mostaplace-work/app/frontend_test_copy/client/public/phones-icons/test')
out.mkdir(parents=True, exist_ok=True)
session = new_session('u2net')
with Image.open(source).convert('RGB') as sheet:
    width, height = sheet.size
    cell_w, cell_h = width / 5, height / 5
    for local_index, name in ((0, 'smartphones'), (4, 'supports-voiture'), (10, 'coques-opaques')):
        row, col = divmod(local_index, 5)
        cell = sheet.crop((round(col * cell_w) + 10, round(row * cell_h) + 10, round((col + 1) * cell_w) - 10, round((row + 1) * cell_h) - 10))
        cutout = remove(cell, session=session, alpha_matting=False).convert('RGBA')
        alpha = cutout.getchannel('A').point(lambda value: 0 if value < 8 else value)
        cutout.putalpha(alpha)
        bbox = alpha.getbbox()
        if bbox:
            cutout = cutout.crop(bbox)
        max_side = max(cutout.size)
        scale = 880 / max_side
        cutout = cutout.resize((round(cutout.width * scale), round(cutout.height * scale)), Image.Resampling.LANCZOS)
        canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
        canvas.alpha_composite(cutout, ((1024-cutout.width)//2, (1024-cutout.height)//2))
        dest = out / f'{name}-nomatting.webp'
        canvas.save(dest, 'WEBP', quality=90, method=6)
        print(dest, dest.stat().st_size)
