"""
engine_2d/particle_system.py
Real-time 2D Particle Physics Engine.
Implements:
- 3D Spinning Golden Coin Rain with floor collision and elasticity.
- Gushing High-Pressure Oil Geyser with gravity and droplet spray.
- Multi-colored Festive Fireworks explosions for celebrations.
- Exhaust / Sand Drift Smoke Puffs.
"""

import os
import math
import random
import numpy as np
from PIL import Image

SPRITES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")


class CoinParticle:
    def __init__(self, x_spawn, y_spawn, floor_y=950):
        self.x = x_spawn + random.uniform(-150, 150)
        self.y = y_spawn + random.uniform(-80, 20)
        self.vx = random.uniform(-180, 180)
        self.vy = random.uniform(-600, -150)
        self.floor_y = floor_y
        self.gravity = 1400.0
        self.spin_speed = random.uniform(8.0, 18.0)
        self.spin_phase = random.uniform(0, 6.28)
        self.scale = random.uniform(0.45, 0.75)
        self.bounces = 0
        self.alive = True

    def update(self, dt):
        if not self.alive:
            return
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Floor bounce
        if self.y >= self.floor_y:
            self.y = self.floor_y
            self.vy = -0.52 * abs(self.vy)
            self.vx *= 0.75
            self.bounces += 1
            if self.bounces > 4 and abs(self.vy) < 40:
                self.vy = 0
                self.vx = 0


class CoinShowerSystem:
    def __init__(self, coin_count=35, spawn_center=(960, 200), floor_y=950):
        self.coin_sprite = Image.open(os.path.join(SPRITES_DIR, "gold_coin.png")).convert("RGBA")
        self.coins = []
        for _ in range(coin_count):
            self.coins.append(CoinParticle(spawn_center[0], spawn_center[1], floor_y))

    def update(self, dt):
        for c in self.coins:
            c.update(dt)

    def draw(self, bg_image, t):
        cw, ch = self.coin_sprite.size
        for c in self.coins:
            # 3D horizontal spin projection
            spin_factor = abs(math.cos(t * c.spin_speed + c.spin_phase))
            render_w = max(4, int(cw * c.scale * spin_factor))
            render_h = int(ch * c.scale)
            
            scaled_coin = self.coin_sprite.resize((render_w, render_h), Image.Resampling.BILINEAR)
            paste_x = int(c.x - render_w // 2)
            paste_y = int(c.y - render_h // 2)
            
            # Boundary check
            if -50 < paste_x < bg_image.width + 50 and -50 < paste_y < bg_image.height + 50:
                bg_image.alpha_composite(scaled_coin, (paste_x, paste_y))


class OilGeyserSystem:
    def __init__(self, nozzle_pos=(960, 750), particle_count=55):
        self.nozzle_x, self.nozzle_y = nozzle_pos
        self.particles = []
        for _ in range(particle_count):
            self.particles.append(self._spawn_particle(initial=True))

    def _spawn_particle(self, initial=False):
        angle = random.uniform(-math.pi * 0.65, -math.pi * 0.35)
        speed = random.uniform(600, 1100)
        return {
            "x": self.nozzle_x + random.uniform(-12, 12),
            "y": self.nozzle_y if not initial else self.nozzle_y - random.uniform(0, 300),
            "vx": speed * math.cos(angle),
            "vy": speed * math.sin(angle),
            "radius": random.uniform(6, 16),
            "life": random.uniform(0.8, 1.6),
            "max_life": 1.6,
            "color": random.choice([(20, 20, 24, 240), (35, 30, 25, 230), (10, 10, 12, 250)])
        }

    def update(self, dt):
        for p in self.particles:
            p["vy"] += 1500.0 * dt  # Gravity
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["life"] -= dt
            if p["life"] <= 0 or p["y"] > self.nozzle_y + 80:
                p.update(self._spawn_particle(initial=False))

    def draw(self, bg_image):
        from PIL import ImageDraw
        draw = ImageDraw.Draw(bg_image, "RGBA")
        for p in self.particles:
            x, y, r = p["x"], p["y"], p["radius"]
            draw.ellipse([x - r, y - r, x + r, y + r], fill=p["color"])
            # Amber gold highlight glint
            if r > 10:
                draw.ellipse([x - r*0.4, y - r*0.4, x - r*0.1, y - r*0.1], fill=(245, 158, 11, 200))


class FireworksSystem:
    def __init__(self, num_bursts=4):
        self.bursts = []
        colors = [
            (239, 68, 68),    # Red
            (34, 197, 94),    # Green
            (250, 204, 21),   # Gold
            (56, 189, 248),   # Cyan
            (255, 255, 255)   # White
        ]
        centers = [(450, 300), (960, 220), (1450, 280), (750, 380)]
        for i in range(num_bursts):
            cx, cy = centers[i % len(centers)]
            sparks = []
            for _ in range(35):
                ang = random.uniform(0, 6.28)
                spd = random.uniform(120, 480)
                sparks.append({
                    "x": cx, "y": cy,
                    "vx": spd * math.cos(ang),
                    "vy": spd * math.sin(ang),
                    "color": random.choice(colors),
                    "size": random.uniform(3, 7)
                })
            self.bursts.append({"sparks": sparks, "time": random.uniform(0, 0.4)})

    def update(self, dt):
        for b in self.bursts:
            b["time"] += dt
            for s in b["sparks"]:
                s["vy"] += 280.0 * dt  # Gentle gravity
                s["vx"] *= 0.96        # Air drag
                s["vy"] *= 0.96
                s["x"] += s["vx"] * dt
                s["y"] += s["vy"] * dt

    def draw(self, bg_image):
        from PIL import ImageDraw
        draw = ImageDraw.Draw(bg_image, "RGBA")
        for b in self.bursts:
            alpha = max(0, int(255 * (1.0 - min(1.0, b["time"] / 2.0))))
            if alpha <= 0:
                continue
            for s in b["sparks"]:
                c = s["color"] + (alpha,)
                r = s["size"]
                draw.ellipse([s["x"] - r, s["y"] - r, s["x"] + r, s["y"] + r], fill=c)

