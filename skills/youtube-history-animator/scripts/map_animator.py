"""
engine_2d/map_animator.py
Dynamic Animated Cartography & Vehicle Entity Kinetics.
Implements:
- Animated sailing dhow boats rocking on animated water waves.
- Bedouin camel walking cycle across desert dunes.
- High-speed gold-plated supercar zoom with tire smoke trails.
- Burj Khalifa kinetic vertical growth assembly.
- Emirates Hope Mars probe orbital flight trajectory.
- Animated progressive dashed trade arrows and connection lines.
"""

import os
import math
from PIL import Image, ImageDraw

SPRITES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


class MapEntityAnimator:
    def __init__(self):
        self.dhow_sprite = Image.open(os.path.join(SPRITES_DIR, "dhow_ship.png")).convert("RGBA")
        self.camel_sprite = Image.open(os.path.join(SPRITES_DIR, "camel.png")).convert("RGBA")
        self.supercar_sprite = Image.open(os.path.join(SPRITES_DIR, "supercar.png")).convert("RGBA")
        self.oil_derrick_sprite = Image.open(os.path.join(SPRITES_DIR, "oil_derrick.png")).convert("RGBA")
        self.burj_sprite = Image.open(os.path.join(SPRITES_DIR, "burj_khalifa.png")).convert("RGBA")
        self.hope_sprite = Image.open(os.path.join(SPRITES_DIR, "hope_satellite.png")).convert("RGBA")
        self.oyster_sprite = Image.open(os.path.join(SPRITES_DIR, "pearl_oyster.png")).convert("RGBA")
        self.uae_flag_sprite = Image.open(os.path.join(SPRITES_DIR, "uae_flag.png")).convert("RGBA")

    def draw_dhow_boat(self, canvas, t, pos=(1200, 480), scale=0.75):
        """Draws a rocking dhow boat traveling on water waves."""
        # Rocking angle and vertical bob
        rock_angle = math.sin(t * 2.8) * 5.0
        bob_y = int(math.cos(t * 2.8) * 8.0)
        
        w, h = self.dhow_sprite.size
        sw, sh = int(w * scale), int(h * scale)
        scaled = self.dhow_sprite.resize((sw, sh), Image.Resampling.BILINEAR)
        rotated = scaled.rotate(rock_angle, resample=Image.Resampling.BILINEAR, expand=True)
        
        x = int(pos[0] + math.sin(t * 0.5) * 40 - rotated.width // 2)
        y = int(pos[1] + bob_y - rotated.height // 2)
        canvas.alpha_composite(rotated, (x, y))

    def draw_camel_walk(self, canvas, t, start_x=-200, target_x=650, y=620, scale=0.85):
        """Draws walking Bedouin camel across desert."""
        # Horizontal progression
        walk_speed = 70.0
        cur_x = int(start_x + (t * walk_speed) % (target_x - start_x + 600))
        if cur_x > target_x:
            cur_x = target_x
        
        # Step bounce and neck nodding
        step_bob = abs(math.sin(t * 5.0)) * 12.0
        nod_angle = math.sin(t * 5.0) * 4.0
        
        w, h = self.camel_sprite.size
        sw, sh = int(w * scale), int(h * scale)
        scaled = self.camel_sprite.resize((sw, sh), Image.Resampling.BILINEAR)
        rotated = scaled.rotate(nod_angle, resample=Image.Resampling.BILINEAR, expand=True)
        
        canvas.alpha_composite(rotated, (int(cur_x), int(y - step_bob)))

    def draw_supercar_drift(self, canvas, t, t_rel, start_x=2100, end_x=700, y=720):
        """Draws high speed gold supercar entering with aggressive brake decelerate."""
        if t_rel < 0.2:
            return
        # Ease out cubic deceleration
        prog = min(1.0, (t_rel - 0.2) / 1.2)
        ease = 1.0 - math.pow(1.0 - prog, 3)
        cur_x = int(start_x + (end_x - start_x) * ease)
        
        w, h = self.supercar_sprite.size
        scale = 0.95
        scaled = self.supercar_sprite.resize((int(w * scale), int(h * scale)), Image.Resampling.BILINEAR)
        
        # Car vibration
        vib_y = int(math.sin(t * 40.0) * 2.0) if prog < 1.0 else 0
        canvas.alpha_composite(scaled, (cur_x, y + vib_y))

    def draw_oil_derrick(self, canvas, t, pos=(1250, 520), scale=0.9):
        """Draws pumping oil derrick."""
        w, h = self.oil_derrick_sprite.size
        sw, sh = int(w * scale), int(h * scale)
        scaled = self.oil_derrick_sprite.resize((sw, sh), Image.Resampling.BILINEAR)
        canvas.alpha_composite(scaled, (pos[0] - sw // 2, pos[1] - sh // 2))

    def draw_burj_khalifa_growth(self, canvas, t_rel, pos=(1450, 320), scale=1.0):
        """Draws Burj Khalifa rising into the sky from the ground."""
        prog = min(1.0, t_rel / 1.8)
        # Elastic settle
        ease = 1.0 - math.exp(-4.5 * prog) * math.cos(3.0 * prog)
        
        w, h = self.burj_sprite.size
        cur_h = max(20, int(h * ease))
        
        # Crop from bottom up
        crop_box = (0, h - cur_h, w, h)
        cropped = self.burj_sprite.crop(crop_box)
        
        target_y = pos[1] + (h - cur_h)
        canvas.alpha_composite(cropped, (pos[0], target_y))

    def draw_hope_mars_probe(self, canvas, t, mars_pos=(1550, 240), probe_scale=0.7):
        """Draws Mars planet and Hope probe in elliptical orbit."""
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # Mars Red Planet
        mx, my = mars_pos
        mr = 90
        draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(225, 75, 45, 255), outline=(180, 50, 25, 255), width=4)
        # Polar Ice Cap
        draw.ellipse([mx - 25, my - mr + 6, mx + 25, my - mr + 28], fill=(245, 245, 250, 220))
        
        # Orbital path line (Dashed)
        rx, ry = 220, 100
        for deg in range(0, 360, 8):
            rad = math.radians(deg)
            px = mx + int(rx * math.cos(rad))
            py = my + int(ry * math.sin(rad))
            draw.point((px, py), fill=(96, 165, 250, 160))

        # Probe position along orbit
        orb_angle = t * 0.8
        probe_x = int(mx + rx * math.cos(orb_angle))
        probe_y = int(my + ry * math.sin(orb_angle))
        
        # Draw golden communication pulse rings
        pulse_r = int((t * 60) % 50)
        draw.ellipse([probe_x - pulse_r, probe_y - pulse_r, probe_x + pulse_r, probe_y + pulse_r],
                     outline=(250, 204, 21, max(0, 255 - pulse_r * 5)), width=2)

        w, h = self.hope_sprite.size
        sw, sh = int(w * probe_scale), int(h * probe_scale)
        scaled = self.hope_sprite.resize((sw, sh), Image.Resampling.BILINEAR)
        canvas.alpha_composite(scaled, (probe_x - sw // 2, probe_y - sh // 2))

    def draw_animated_trade_route(self, canvas, t, start_pt, end_pt, color=(250, 204, 21, 230)):
        """Draws animated dashed vector arrow between two points."""
        draw = ImageDraw.Draw(canvas, "RGBA")
        x1, y1 = start_pt
        x2, y2 = end_pt
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)
        if dist < 1:
            return

        ux, uy = dx / dist, dy / dist
        dash_len = 16
        gap_len = 12
        period = dash_len + gap_len
        offset = (t * 70.0) % period

        d = -offset
        while d < dist:
            seg_start = max(0.0, d)
            seg_end = min(dist, d + dash_len)
            if seg_end > seg_start:
                p1 = (int(x1 + ux * seg_start), int(y1 + uy * seg_start))
                p2 = (int(x1 + ux * seg_end), int(y1 + uy * seg_end))
                draw.line([p1, p2], fill=color, width=5)
            d += period

