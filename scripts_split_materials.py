from pathlib import Path
from PIL import Image, ImageFilter
from rembg import remove

SOURCE = Path('/home/ubuntu/upload/pasted_file_i5IVzz_ChatGPTImage22août2026,17_54_41.png')
OUTPUT = Path('/home/ubuntu/mostaplace-work/app/frontend_test_copy/client/public/materials-icons/cutouts')
OUTPUT.mkdir(parents=True, exist_ok=True)

ITEMS = [
    ('perceuses', 'Perceuses'),
    ('cles-a-molette', 'Clés à molette'),
    ('marteaux', 'Marteaux'),
    ('metres-rubans', 'Mètres rubans'),
    ('tournevis', 'Tournevis'),
    ('boites-a-outils', 'Boîtes à outils'),
    ('cles-mixtes', 'Clés mixtes'),
    ('meuleuses', 'Meuleuses'),
    ('pinces', 'Pinces'),
    ('sets-tournevis', 'Sets de tournevis'),
    ('servantes-d-atelier', 'Servantes d’atelier'),
    ('perceuses-visseuses', 'Perceuses-visseuses'),
    ('scies-circulaires', 'Scies circulaires'),
    ('coffrets-douilles', 'Coffrets de douilles'),
    ('cutters', 'Cutters'),
    ('niveaux-a-bulle', 'Niveaux à bulle'),
    ('equerres', 'Équerres'),
    ('rouleaux-de-peinture', 'Rouleaux de peinture'),
    ('pinces-multiprises', 'Pinces multiprises'),
    ('agrafeuses', 'Agrafeuses'),
    ('gants-de-travail', 'Gants de travail'),
    ('casques-de-chantier', 'Casques de chantier'),
    ('lunettes-de-protection', 'Lunettes de protection'),
    ('bottes-de-chantier', 'Bottes de chantier'),
    ('sacs-a-outils', 'Sacs à outils'),
]

with Image.open(SOURCE).convert('RGB') as sheet:
    width, height = sheet.size
    cell_w, cell_h = width / 5, height / 5
    for index, (slug, label) in enumerate(ITEMS):
        row, col = divmod(index, 5)
        x0 = round(col * cell_w) + 10
        y0 = round(row * cell_h) + 10
        x1 = round((col + 1) * cell_w) - 10
        y1 = round((row + 1) * cell_h) - 10
        cell = sheet.crop((x0, y0, x1, y1))
        cutout = remove(cell, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=8, alpha_matting_erode_size=3).convert('RGBA')
        alpha = cutout.getchannel('A').point(lambda value: 0 if value < 18 else value)
        cutout.putalpha(alpha)
        bbox = alpha.getbbox()
        if bbox:
            cutout = cutout.crop(bbox)
        max_side = max(cutout.size)
        target_subject = 880
        scale = (target_subject / max_side) if max_side else 1.0
        new_size = (max(1, round(cutout.width * scale)), max(1, round(cutout.height * scale)))
        cutout = cutout.resize(new_size, Image.Resampling.LANCZOS)
        canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
        left = (1024 - cutout.width) // 2
        top = (1024 - cutout.height) // 2
        canvas.alpha_composite(cutout, (left, top))
        destination = OUTPUT / f'{slug}.webp'
        canvas.save(destination, 'WEBP', quality=90, method=6)
        print(f'{index + 1:02d} {label} -> {destination.name} {destination.stat().st_size} bytes')
