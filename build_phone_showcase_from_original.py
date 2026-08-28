from pathlib import Path
from PIL import Image
from rembg import remove, new_session

source = Path('/home/ubuntu/upload/pasted_file_942F3a_ChatGPTImage22août2026,18_55_38.png')
target = Path('/home/ubuntu/mostaplace-work/app/frontend_test_copy/client/public/phones-icons/phones-accessories-showcase-transparent.webp')
canvas_size = 1920
cols = rows = 5
with Image.open(source).convert('RGB') as sheet:
    cell_w = sheet.width / cols
    cell_h = sheet.height / rows
    canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
    session = new_session('u2net')
    for index in range(rows * cols):
        row, col = divmod(index, cols)
        x0, y0 = round(col * cell_w), round(row * cell_h)
        x1, y1 = round((col + 1) * cell_w), round((row + 1) * cell_h)
        cell = sheet.crop((x0, y0, x1, y1))
        cutout = remove(cell, session=session, alpha_matting=False).convert('RGBA')
        alpha = cutout.getchannel('A').point(lambda value: 0 if value < 8 else value)
        cutout.putalpha(alpha)
        target_box = (round(col * canvas_size / cols), round(row * canvas_size / rows), round((col + 1) * canvas_size / cols), round((row + 1) * canvas_size / rows))
        cutout = cutout.resize((target_box[2] - target_box[0], target_box[3] - target_box[1]), Image.Resampling.LANCZOS)
        canvas.alpha_composite(cutout, (target_box[0], target_box[1]))

target.parent.mkdir(parents=True, exist_ok=True)
canvas.save(target, 'WEBP', lossless=True, method=6)
print(f'{target} {canvas.width}x{canvas.height} {target.stat().st_size} bytes')
