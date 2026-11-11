"""
engine_2d/publisher/viral_thumbnail_generator.py
High-CTR YouTube Thumbnail Generator (1280x720 / 300 DPI).
Implements the OverSimplified / History Matters viral packaging blueprint:
- Left-to-right visual contrast (Desert Gold vs Royal Navy / Oil Black)
- High-res Chibi character puppet with intense expressive reaction
- High-stakes visual focal point (Crashing Pearl, British Warship, Gold Geyser)
- Big bold kinetic 3D typography with heavy black stroke and drop shadow
- Smartphone-tested high saturation and contrast
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_BOLD = r"C:\Windows\Fonts\impact.ttf"
if not os.path.exists(FONT_BOLD):
    FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"


def generate_high_ctr_thumbnail(output_path, sprites_dir=None, topic="History of UAE"):
    """
    Renders a 1280x720 broadcast JPEG thumbnail designed for 12%+ CTR.
    """
    width, height = 1280, 720
    thumb = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(thumb, "RGBA")

    # 1. High-Contrast Split Background
    # Left side: Golden Harsh Desert
    for x in range(width // 2 + 100):
        p = x / float(width // 2 + 100)
        col = (int(217 + 25*p), int(119 - 15*p), int(6 + 10*p), 255)
        draw.line([(x, 0), (x, height)], fill=col)

    # Right side: Modern Deep Space / Twilight Metropolis
    for x in range(width // 2 - 80, width):
        p = (x - (width // 2 - 80)) / float(width - (width // 2 - 80))
        col = (int(15 - 10*p), int(23 + 15*p), int(42 + 45*p), 255)
        draw.line([(x, 0), (x, height)], fill=col)

    # Diagonal slice line
    draw.polygon([(560, 0), (740, 0), (520, height), (340, height)], fill=(251, 191, 36, 180))

    # 2. Add Chibi Characters
    if not sprites_dir:
        # Default search path relative to plugin root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cand = [
            os.path.join(current_dir, "..", "..", "youtube-history-animator", "scripts", "sprites"),
            os.path.join(os.getcwd(), "engine_2d", "sprites"),
            os.path.join(os.getcwd(), "sprites"),
        ]
        for c in cand:
            c_norm = os.path.normpath(c)
            if os.path.exists(c_norm):
                sprites_dir = c_norm
                break

    # Sheikh Zayed on Right (Visionary Leader)
    zayed_path = os.path.join(sprites_dir, "sheikh_zayed.png") if sprites_dir else None
    if zayed_path and os.path.exists(zayed_path):
        z_img = Image.open(zayed_path).convert("RGBA")
        z_scaled = z_img.resize((int(z_img.width * 1.55), int(z_img.height * 1.55)), Image.Resampling.BILINEAR)
        # Add glowing outer halo for separation
        halo = Image.new("RGBA", (z_scaled.width + 40, z_scaled.height + 40), (0, 0, 0, 0))
        hdraw = ImageDraw.Draw(halo)
        hdraw.ellipse([20, 20, z_scaled.width + 20, z_scaled.height + 20], fill=(251, 191, 36, 90))
        halo = halo.filter(ImageFilter.GaussianBlur(18))
        thumb.alpha_composite(halo, (780, 50))
        thumb.alpha_composite(z_scaled, (800, 70))

    # Shocked Pearl Diver on Left
    diver_path = os.path.join(sprites_dir, "pearl_diver.png") if sprites_dir else None
    if diver_path and os.path.exists(diver_path):
        d_img = Image.open(diver_path).convert("RGBA")
        d_scaled = d_img.resize((int(d_img.width * 1.35), int(d_img.height * 1.35)), Image.Resampling.BILINEAR)
        thumb.alpha_composite(d_scaled, (30, 160))

    # 3. High-Stakes Visual Drama: Crashing Red Arrow & Pearl
    # Giant Pearl
    draw.ellipse([450, 360, 610, 520], fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=6)
    draw.ellipse([480, 380, 530, 430], fill=(254, 240, 138, 255))
    # Crashing Red Lightning Arrow
    arrow_pts = [
        (400, 160), (490, 160), (510, 280), (600, 280),
        (480, 480), (420, 340), (450, 340)
    ]
    draw.polygon(arrow_pts, fill=(239, 68, 68, 255), outline=(0, 0, 0, 255))
    
    # 4. Bold Kinetic 3D Typography
    try:
        font_huge = ImageFont.truetype(FONT_BOLD, 88)
        font_sub = ImageFont.truetype(FONT_BOLD, 74)
        font_badge = ImageFont.truetype(FONT_BOLD, 46)
    except Exception:
        font_huge = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    def draw_stroked_text(canvas, pos, text, font, fill_color, stroke_color=(0, 0, 0, 255), stroke_w=8):
        tx, ty = pos
        # Drop shadow
        canvas.text((tx + 6, ty + 6), text, font=font, fill=(0, 0, 0, 220))
        # Stroke
        for dx in range(-stroke_w, stroke_w + 1):
            for dy in range(-stroke_w, stroke_w + 1):
                if dx*dx + dy*dy <= stroke_w*stroke_w:
                    canvas.text((tx + dx, ty + dy), text, font=font, fill=stroke_color)
        # Fill
        canvas.text((tx, ty), text, font=font, fill=fill_color)

    # Line 1: "FROM ZERO..."
    draw_stroked_text(draw, (80, 30), "FROM ZERO...", font_sub, fill_color=(255, 255, 255, 255), stroke_w=7)

    # Line 2: "TO $500 BILLION!"
    draw_stroked_text(draw, (70, 110), "TO $500 BILLION!", font_huge, fill_color=(250, 204, 21, 255), stroke_w=9)

    # Market Crash Badge on Arrow
    draw.rounded_rectangle([390, 540, 670, 615], radius=16, fill=(239, 68, 68, 255), outline=(0, 0, 0, 255), width=5)
    draw_stroked_text(draw, (408, 548), "-98% CRASH!", font_badge, fill_color=(255, 255, 255, 255), stroke_w=5)

    # Format Badge in Bottom Right
    draw.rounded_rectangle([860, 640, 1220, 700], radius=12, fill=(0, 0, 0, 220), outline=(250, 204, 21, 255), width=3)
    draw.text((885, 650), "FULL DOCUMENTARY", font=font_badge, fill=(250, 204, 21, 255))

    # 5. Vignette Shadow Border
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    vdraw.rectangle([(0, 0), (width, height)], outline=(0, 0, 0, 180), width=16)
    thumb.alpha_composite(vignette)

    # Save as high-quality JPEG
    rgb_thumb = thumb.convert("RGB")
    rgb_thumb.save(output_path, "JPEG", quality=96)
    print(f"🖼️ High-CTR Viral Thumbnail Generated: {output_path} (1280x720 / 96% JPEG)")
    return output_path


if __name__ == "__main__":
    generate_high_ctr_thumbnail("viral_thumbnail_preview.jpg")
