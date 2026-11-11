"""
generate_ctr_thumbnail.py
Generates a broadcast-grade, high-CTR YouTube thumbnail (1280x720) in the iconic
OverSimplified / History Matters style:
- High contrast split-screen: 1930s Great Pearl Crash (gloomy stormy teal) vs. 2024 Megacity Miracle (rich gold/space)
- Chibi expressive character rigs (Bedouin pearl diver fainting in shock vs. Sheikh Zayed with gold bisht)
- Iconic landmark visual anchors (Burj Khalifa towering into space, golden supercar, cascading 3D gold coins)
- High-impact bold typography: "DESERT TO MARS!" with heavy drop shadow and vibrant yellow/gold fill (#FACC15)
- Psychological curiosity stamps: "CRASH: -95%" and "$1,000,000,000,000+"
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SPRITES_DIR = r"c:\Users\shubh\OneDrive\Desktop\animator\engine_2d\sprites"
OUT_THUMBNAIL = r"c:\Users\shubh\OneDrive\Desktop\animator\uae_12min_production\thumbnail.jpg"
ARTIFACT_THUMBNAIL = r"C:\Users\shubh\.gemini\antigravity\brain\42c491fb-d1b2-4020-8a19-3044f8f05305\assets\thumbnail_desert_to_mars.jpg"

W, H = 1280, 720

def create_thumbnail():
    canvas = Image.new("RGBA", (W, H))
    draw = ImageDraw.Draw(canvas)

    # 1. Background: Diagonal Dynamic Split
    # Left side: 1930s gloomy oceanic storm (poverty, crash)
    for x in range(W // 2 + 100):
        prog = x / float(W // 2 + 100)
        r = int(15 + 10 * prog)
        g = int(25 + 15 * prog)
        b = int(35 + 25 * prog)
        draw.line([(x, 0), (x, H)], fill=(r, g, b, 255))

    # Right side: 2024 Golden Twilight Desert & Cosmic Space
    for x in range(W // 2 - 100, W):
        prog = (x - (W // 2 - 100)) / float(W // 2 + 100)
        r = int(20 + (50 - 20) * prog)
        g = int(15 + (35 - 15) * prog)
        b = int(30 + (70 - 30) * prog)
        draw.line([(x, 0), (x, H)], fill=(r, g, b, 255))

    # Angled yellow-gold energy divider line down the middle
    divider_pts = [(W // 2 - 60, 0), (W // 2 - 40, 0), (W // 2 + 40, H), (W // 2 + 20, H)]
    draw.polygon(divider_pts, fill=(245, 158, 11, 255))
    glow_pts = [(W // 2 - 80, 0), (W // 2 - 20, 0), (W // 2 + 60, H), (W // 2, H)]
    draw.polygon(glow_pts, fill=(250, 204, 21, 60))

    # 2. Add Left Elements: 1930s Pearl Diver Shocked & Empty Oyster
    diver_body = Image.open(os.path.join(SPRITES_DIR, "pearl_diver_body.png")).convert("RGBA")
    diver_head = Image.open(os.path.join(SPRITES_DIR, "pearl_diver_head.png")).convert("RGBA")
    diver_shocked = Image.open(os.path.join(SPRITES_DIR, "eyes_shocked.png")).convert("RGBA")
    oyster = Image.open(os.path.join(SPRITES_DIR, "pearl_oyster.png")).convert("RGBA")

    # Assemble diver puppet
    diver_comp = Image.new("RGBA", (450, 600), (0, 0, 0, 0))
    diver_comp.alpha_composite(diver_body, (40, 160))
    diver_head_c = diver_head.copy()
    diver_head_c.alpha_composite(diver_shocked, (int(diver_head.width * 0.44 - diver_shocked.width // 2), int(diver_head.height * 0.44 - diver_shocked.height // 2)))
    diver_comp.alpha_composite(diver_head_c, (50, 20))

    # Scale diver
    diver_scaled = diver_comp.resize((int(diver_comp.width * 0.85), int(diver_comp.height * 0.85)), Image.Resampling.BILINEAR)
    canvas.alpha_composite(diver_scaled, (60, 220))

    # Empty oyster shell
    oyster_scaled = oyster.resize((int(oyster.width * 0.9), int(oyster.height * 0.9)), Image.Resampling.BILINEAR)
    canvas.alpha_composite(oyster_scaled, (20, 480))

    # 3. Add Right Elements: Sheikh Zayed, Burj Khalifa, Supercar, Coins
    burj = Image.open(os.path.join(SPRITES_DIR, "burj_khalifa_tower.png")).convert("RGBA")
    burj_scaled = burj.resize((int(burj.width * 0.85), int(burj.height * 0.85)), Image.Resampling.BILINEAR)
    canvas.alpha_composite(burj_scaled, (1020, 20))

    zayed_body = Image.open(os.path.join(SPRITES_DIR, "sheikh_zayed_body.png")).convert("RGBA")
    zayed_head = Image.open(os.path.join(SPRITES_DIR, "sheikh_zayed_head.png")).convert("RGBA")
    dollar_eyes = Image.open(os.path.join(SPRITES_DIR, "eyes_dollar.png")).convert("RGBA")

    zayed_comp = Image.new("RGBA", (450, 650), (0, 0, 0, 0))
    zayed_comp.alpha_composite(zayed_body, (30, 180))
    zayed_head_c = zayed_head.copy()
    zayed_head_c.alpha_composite(dollar_eyes, (int(zayed_head.width * 0.44 - dollar_eyes.width // 2), int(zayed_head.height * 0.44 - dollar_eyes.height // 2)))
    zayed_comp.alpha_composite(zayed_head_c, (40, 20))

    zayed_scaled = zayed_comp.resize((int(zayed_comp.width * 0.9), int(zayed_comp.height * 0.9)), Image.Resampling.BILINEAR)
    canvas.alpha_composite(zayed_scaled, (680, 170))

    # Gold Supercar cruising
    supercar = Image.open(os.path.join(SPRITES_DIR, "supercar.png")).convert("RGBA")
    car_scaled = supercar.resize((int(supercar.width * 0.7), int(supercar.height * 0.7)), Image.Resampling.BILINEAR)
    canvas.alpha_composite(car_scaled, (760, 520))

    # Gold Coins flying
    coin = Image.open(os.path.join(SPRITES_DIR, "gold_coin.png")).convert("RGBA")
    c_scaled1 = coin.resize((70, 70), Image.Resampling.BILINEAR)
    c_scaled2 = coin.resize((50, 50), Image.Resampling.BILINEAR)
    canvas.alpha_composite(c_scaled1, (620, 320))
    canvas.alpha_composite(c_scaled2, (960, 260))
    canvas.alpha_composite(c_scaled1, (1080, 420))

    # 4. Stamp Badges: Left Crash vs Right Wealth
    # Left Stamp: "CRASH: -95%" (Angled Red)
    stamp_red = Image.new("RGBA", (280, 80), (0, 0, 0, 0))
    sdraw_r = ImageDraw.Draw(stamp_red)
    sdraw_r.rounded_rectangle([4, 4, 276, 76], radius=12, outline=(239, 68, 68, 255), width=6, fill=(15, 10, 10, 210))
    try:
        font_stamp = ImageFont.truetype("arialbd.ttf", 34)
    except:
        font_stamp = ImageFont.load_default()
    sdraw_r.text((22, 20), "CRASH: -95%", font=font_stamp, fill=(239, 68, 68, 255))
    rotated_r = stamp_red.rotate(14, resample=Image.Resampling.BILINEAR, expand=True)
    canvas.alpha_composite(rotated_r, (180, 140))

    # Right Stamp: "$1,000,000,000,000+" (Angled Gold)
    stamp_gold = Image.new("RGBA", (340, 80), (0, 0, 0, 0))
    sdraw_g = ImageDraw.Draw(stamp_gold)
    sdraw_g.rounded_rectangle([4, 4, 336, 76], radius=12, outline=(250, 204, 21, 255), width=6, fill=(15, 15, 10, 210))
    sdraw_g.text((18, 20), "$1 TRILLION+", font=font_stamp, fill=(250, 204, 21, 255))
    rotated_g = stamp_gold.rotate(-12, resample=Image.Resampling.BILINEAR, expand=True)
    canvas.alpha_composite(rotated_g, (780, 110))

    # 5. Epic Typography: "DESERT TO MARS!" at Bottom Center
    # Multi-layered text: Black drop shadow -> Red glow -> Solid #FACC15 Yellow
    try:
        font_title = ImageFont.truetype("impact.ttf", 112)
    except:
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 100)
        except:
            font_title = ImageFont.load_default()

    title_text = "DESERT TO MARS!"
    t_bbox = font_title.getbbox(title_text)
    tw = t_bbox[2] - t_bbox[0]
    th = t_bbox[3] - t_bbox[1]
    tx = (W - tw) // 2
    ty = H - th - 55

    # Heavy dark badge behind headline for 100% CTR contrast
    t_box = [tx - 40, ty - 15, tx + tw + 40, ty + th + 25]
    draw.rounded_rectangle(t_box, radius=20, fill=(10, 10, 15, 235), outline=(250, 204, 21, 255), width=5)

    # Black outlines & Drop Shadow
    for dx, dy in [(-5, 0), (5, 0), (0, -5), (0, 5), (-4, -4), (4, 4), (-4, 4), (4, -4), (0, 8), (0, 12)]:
        draw.text((tx + dx, ty + dy), title_text, font=font_title, fill=(0, 0, 0, 255))

    # Radiant Yellow Fill with Ka-pow
    draw.text((tx, ty), title_text, font=font_title, fill=(250, 204, 21, 255))

    # 6. Save in RGB 1280x720 JPEG
    final_rgb = canvas.convert("RGB")
    final_rgb.save(OUT_THUMBNAIL, quality=95)
    final_rgb.save(ARTIFACT_THUMBNAIL, quality=95)
    print(f"✅ High-CTR Thumbnail Generated: {OUT_THUMBNAIL}")
    print(f"✅ Artifact Thumbnail Saved: {ARTIFACT_THUMBNAIL}")

if __name__ == "__main__":
    create_thumbnail()
