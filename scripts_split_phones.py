from pathlib import Path
from PIL import Image
from rembg import remove, new_session

SOURCES = [
    (Path('/home/ubuntu/upload/pasted_file_942F3a_ChatGPTImage22août2026,18_55_38.png'), 5),
    (Path('/home/ubuntu/upload/pasted_file_otz67Q_ChatGPTImage22août2026,18_56_03.png'), 4),
]
OUTPUT = Path('/home/ubuntu/mostaplace-work/app/frontend_test_copy/client/public/phones-icons/cutouts')
OUTPUT.mkdir(parents=True, exist_ok=True)

ITEMS = [
    ('smartphones', 'Smartphones'),
    ('smartphones-pliables', 'Smartphones pliables'),
    ('iphones', 'iPhones'),
    ('android', 'Téléphones Android'),
    ('supports-voiture', 'Supports voiture'),
    ('ecouteurs-sans-fil', 'Écouteurs sans fil'),
    ('ecouteurs-bluetooth', 'Écouteurs Bluetooth'),
    ('montres-connectees', 'Montres connectées'),
    ('chargeurs-secteur', 'Chargeurs secteur'),
    ('batteries-externes', 'Batteries externes'),
    ('coques-opaques', 'Coques opaques'),
    ('coques-transparentes', 'Coques transparentes'),
    ('protections-ecran', 'Protections écran'),
    ('cables-usb-c', 'Câbles USB-C'),
    ('cables-usb', 'Câbles USB'),
    ('casques-audio', 'Casques audio'),
    ('enceintes-bluetooth', 'Enceintes Bluetooth'),
    ('chargeurs-voiture', 'Chargeurs voiture'),
    ('cartes-sim', 'Cartes SIM'),
    ('supports-telephone', 'Supports téléphone'),
    ('stylets', 'Stylets'),
    ('trepieds-telephone', 'Trépieds téléphone'),
    ('chargeurs-sans-fil', 'Chargeurs sans fil'),
    ('portefeuilles-telephone', 'Portefeuilles téléphone'),
    ('kits-nettoyage', 'Kits de nettoyage'),
    ('iphone-pro', 'iPhone Pro'),
    ('galaxy-ultra', 'Galaxy Ultra'),
    ('xiaomi', 'Xiaomi'),
    ('oneplus', 'OnePlus'),
    ('google-pixel', 'Google Pixel'),
    ('iphone-standard', 'iPhone'),
    ('galaxy', 'Samsung Galaxy'),
    ('poco', 'POCO'),
    ('realme', 'Realme'),
    ('infinix', 'Infinix'),
    ('vivo', 'Vivo'),
    ('honor', 'Honor'),
    ('motorola', 'Motorola'),
    ('oppo', 'Oppo'),
    ('redmi', 'Redmi'),
    ('tecno-camon', 'Tecno Camon'),
    ('nothing-phone', 'Nothing Phone'),
    ('huawei', 'Huawei'),
    ('iqoo', 'iQOO'),
    ('zte', 'ZTE'),
]

session = new_session('u2net')
item_index = 0
for source, rows in SOURCES:
    with Image.open(source).convert('RGB') as sheet:
        width, height = sheet.size
        cols = 5
        cell_w, cell_h = width / cols, height / rows
        for local_index in range(rows * cols):
            slug, label = ITEMS[item_index]
            row, col = divmod(local_index, cols)
            x0 = round(col * cell_w) + 10
            y0 = round(row * cell_h) + 10
            x1 = round((col + 1) * cell_w) - 10
            y1 = round((row + 1) * cell_h) - 10
            cell = sheet.crop((x0, y0, x1, y1))
            cutout = remove(cell, session=session, alpha_matting=False).convert('RGBA')
            alpha = cutout.getchannel('A').point(lambda value: 0 if value < 4 else value)
            cutout.putalpha(alpha)
            bbox = alpha.getbbox()
            if bbox:
                cutout = cutout.crop(bbox)
            max_side = max(cutout.size)
            target_subject = 820
            scale = (target_subject / max_side) if max_side else 1.0
            new_size = (max(1, round(cutout.width * scale)), max(1, round(cutout.height * scale)))
            cutout = cutout.resize(new_size, Image.Resampling.LANCZOS)
            canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
            left = (1024 - cutout.width) // 2
            top = (1024 - cutout.height) // 2
            canvas.alpha_composite(cutout, (left, top))
            destination = OUTPUT / f'{slug}.webp'
            canvas.save(destination, 'WEBP', quality=92, method=6)
            print(f'{item_index + 1:02d} {label} -> {destination.name} {destination.stat().st_size} bytes', flush=True)
            item_index += 1

print(f'Exported {item_index} assets')
