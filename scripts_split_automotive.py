from pathlib import Path
from PIL import Image
from rembg import remove, new_session

SOURCE = Path('/home/ubuntu/upload/pasted_file_F6aFCg_image.png')
OUTPUT = Path('/home/ubuntu/mostaplace-work/app/frontend_test_copy/client/public/automotive-icons/cutouts')
OUTPUT.mkdir(parents=True, exist_ok=True)

ITEMS = [
    ('pneus', 'Pneus'),
    ('disques-de-frein', 'Disques de frein'),
    ('phares', 'Phares'),
    ('batteries', 'Batteries'),
    ('amortisseurs', 'Amortisseurs'),
    ('turbos', 'Turbos'),
    ('sieges-auto', 'Sièges auto'),
    ('alternateurs', 'Alternateurs'),
    ('jantes', 'Jantes'),
    ('silencieux-echappements', 'Silencieux & échappements'),
    ('boites-de-vitesses', 'Boîtes de vitesses'),
    ('filtres-a-air', 'Filtres à air'),
    ('volants', 'Volants'),
    ('blocs-moteurs', 'Blocs moteurs'),
    ('radiateurs', 'Radiateurs'),
    ('bougies-et-bobines', 'Bougies & bobines'),
    ('plaquettes-de-frein', 'Plaquettes de frein'),
    ('injecteurs', 'Injecteurs'),
    ('cardans', 'Cardans'),
    ('portes-de-voiture', 'Portes de voiture'),
    ('filtres-a-huile', 'Filtres à huile'),
    ('bras-de-suspension', 'Bras de suspension'),
    ('huiles-moteur', 'Huiles moteur'),
    ('kits-de-distribution', 'Kits de distribution'),
    ('retroviseurs', 'Rétroviseurs'),
]

session = new_session('u2net')
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
        cutout = remove(cell, session=session, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=8, alpha_matting_erode_size=3).convert('RGBA')
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
        print(f'{index + 1:02d} {label} -> {destination.name} {destination.stat().st_size} bytes', flush=True)
