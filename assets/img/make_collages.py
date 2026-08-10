from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw


SRC = Path(r"C:\Users\Sebastian\AppData\Local\Temp\codex-collage-inputs")
OUT = Path(__file__).resolve().parent / "collage-output"
FILES = [
    "jorgen-hendriksen-3xxG3Mw7nOg-unsplash.jpg",
    "dina-badamshina-NHfg6b3WCC0-unsplash.jpg",
    "leo-sokolovsky-BaSZo808Oy8-unsplash.jpg",
    "maico-amorim-SJWPKMb9u-k-unsplash.jpg",
]


def grade(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(0.92)
    return ImageEnhance.Sharpness(im).enhance(1.05)


def cover(im: Image.Image, size: tuple[int, int], center=(0.5, 0.5)) -> Image.Image:
    return ImageOps.fit(im, size, method=Image.Resampling.LANCZOS, centering=center)


def paste_panel(canvas, photo, polygon, crop_size, center=(0.5, 0.5)):
    panel = cover(photo, crop_size, center)
    x0 = min(p[0] for p in polygon)
    y0 = min(p[1] for p in polygon)
    mask = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(mask).polygon(polygon, fill=255)
    layer = Image.new("RGB", canvas.size)
    layer.paste(panel, (x0, y0))
    canvas.paste(layer, (0, 0), mask)


def desktop(images):
    w, h, seam = 1920, 1080, 18
    c = Image.new("RGB", (w, h), (5, 7, 9))
    # Large editorial anchor at left, three energetic supporting bands at right.
    paste_panel(c, images[0], [(0, 0), (1120, 0), (900, h), (0, h)], (1120, h), (0.52, 0.48))
    paste_panel(c, images[1], [(1138, 0), (w, 0), (w, 345), (1066, 310)], (854, 345), (0.5, 0.46))
    paste_panel(c, images[2], [(1062, 328), (w, 363), (w, 710), (990, 675)], (930, 382), (0.52, 0.5))
    paste_panel(c, images[3], [(986, 693), (w, 728), (w, h), (914, h)], (1006, 387), (0.5, 0.52))
    return c


def mobile(images):
    w, h = 1080, 1920
    c = Image.new("RGB", (w, h), (5, 7, 9))
    # Portrait-friendly rhythm: dominant opening image followed by three diagonal bands.
    paste_panel(c, images[0], [(0, 0), (w, 0), (w, 850), (0, 760)], (w, 850), (0.5, 0.46))
    paste_panel(c, images[1], [(0, 782), (w, 872), (w, 1210), (0, 1120)], (w, 428), (0.5, 0.48))
    paste_panel(c, images[2], [(0, 1142), (w, 1232), (w, 1570), (0, 1480)], (w, 428), (0.52, 0.5))
    paste_panel(c, images[3], [(0, 1502), (w, 1592), (w, h), (0, h)], (w, 418), (0.5, 0.52))
    return c


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    images = [grade(Image.open(SRC / name)) for name in FILES]
    desktop(images).save(OUT / "collage-portada-pc.jpg", quality=94, subsampling=0, optimize=True)
    mobile(images).save(OUT / "collage-portada-celular.jpg", quality=94, subsampling=0, optimize=True)


if __name__ == "__main__":
    main()
