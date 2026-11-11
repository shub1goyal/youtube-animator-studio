"""
engine_2d/physics_rig.py
Physics-Aware 2D Character Kinetics & Ragdoll Engine.
Implements:
- Damped Harmonic Oscillators for breathing, walking, and speech bobbing
- Squash & Stretch with volume preservation (scale_x * scale_y = 1.0)
- Angular inertia and spring-damper joint rotations for limbs and head tilts
- Gravity-driven ragdoll tumble and ground collision with restitution (bouncing)
- Dynamic pupil tracking and procedural facial expression morphing
"""

import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def apply_alpha_edge_rim_light(puppet_img, char_x, light_x, rim_color=(251, 191, 36), rim_opacity=0.75, shift_px=5):
    """
    Automatic Alpha-Edge Character Rim-Lighting (NumPy Fast Operation):
    Takes character puppet's RGBA image, shifts alpha channel by dx = sign(char_x - light_x) * 5,
    computes rim_mask = alpha_current & (~alpha_shifted), and blends warm/cool rim color along
    illuminated contour at rim_opacity (default 75%).
    """
    if puppet_img is None:
        return None
    arr = np.array(puppet_img, copy=True)
    if arr.ndim != 3 or arr.shape[2] != 4:
        return puppet_img
    alpha = arr[:, :, 3]
    if not np.any(alpha > 20):
        return puppet_img

    # Light direction: if character is to the right of light, light strikes left edge
    dx = int(np.sign(char_x - light_x) * shift_px)
    if dx == 0:
        dx = -shift_px

    shifted = np.zeros_like(alpha)
    if dx > 0:
        shifted[:, dx:] = alpha[:, :-dx]
    else:
        shifted[:, :dx] = alpha[:, -dx:]

    # Edge contour facing the light source
    rim_mask = (alpha > 40) & (shifted < 160)
    if np.any(rim_mask):
        r_c, g_c, b_c = rim_color[:3]
        alpha_factor = rim_opacity
        arr[rim_mask, 0] = np.clip(arr[rim_mask, 0] * (1.0 - alpha_factor) + r_c * alpha_factor, 0, 255).astype(np.uint8)
        arr[rim_mask, 1] = np.clip(arr[rim_mask, 1] * (1.0 - alpha_factor) + g_c * alpha_factor, 0, 255).astype(np.uint8)
        arr[rim_mask, 2] = np.clip(arr[rim_mask, 2] * (1.0 - alpha_factor) + b_c * alpha_factor, 0, 255).astype(np.uint8)
        arr[rim_mask, 3] = np.maximum(arr[rim_mask, 3], int(255 * alpha_factor))

    return Image.fromarray(arr, "RGBA")


def render_contact_shadow(canvas, center_x, ground_y, rx=90, ry=22, sigma=14, opacity=0.72):
    """
    Renders an elliptical soft contact shadow (rgba(5, 6, 12, 0.72), Gaussian blurred sigma=14)
    directly beneath character or prop anchor (X, Y + half_height - 15).
    """
    pad = int(sigma * 3)
    sw = int(rx * 2 + pad * 2)
    sh = int(ry * 2 + pad * 2)
    shadow_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    sdraw.ellipse([pad, pad, pad + rx * 2, pad + ry * 2], fill=(5, 6, 12, int(255 * opacity)))
    shadow_blurred = shadow_img.filter(ImageFilter.GaussianBlur(sigma))
    canvas.alpha_composite(shadow_blurred, (int(center_x - rx - pad), int(ground_y - ry - pad + 5)))


class SpringDamper:
    """Simulates a 1D or 2D damped harmonic spring system: m*a + c*v + k*(x - target) = 0."""
    def __init__(self, stiffness=120.0, damping=14.0, mass=1.0, initial_pos=0.0):
        self.k = stiffness
        self.c = damping
        self.m = mass
        self.pos = float(initial_pos)
        self.vel = 0.0
        self.target = float(initial_pos)

    def update(self, dt):
        force = -self.k * (self.pos - self.target) - self.c * self.vel
        accel = force / self.m
        self.vel += accel * dt
        self.pos += self.vel * dt
        return self.pos

    def snap_to(self, val):
        self.pos = float(val)
        self.target = float(val)
        self.vel = 0.0

    def impulse(self, strength):
        self.vel += strength


class RagdollEntity:
    """
    Simulates a character or prop knocked into a ragdoll state:
    Gravity acceleration, angular torque, floor bounce with energy loss (restitution).
    """
    def __init__(self, x, y, floor_y=880, restitution=0.45, friction=0.85):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.angle = 0.0
        self.v_rot = 0.0
        self.floor_y = floor_y
        self.restitution = restitution
        self.friction = friction
        self.gravity = 1400.0  # px/s^2
        self.is_grounded = False

    def launch(self, vx, vy, torque):
        self.vx = vx
        self.vy = vy
        self.v_rot = torque
        self.is_grounded = False

    def update(self, dt):
        if not self.is_grounded:
            self.vy += self.gravity * dt
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.angle += self.v_rot * dt

            # Floor collision
            if self.y >= self.floor_y:
                self.y = self.floor_y
                if abs(self.vy) > 80.0:
                    self.vy = -self.vy * self.restitution
                    self.vx *= self.friction
                    self.v_rot *= self.friction * 0.7
                else:
                    self.vy = 0.0
                    self.vx = 0.0
                    self.v_rot = 0.0
                    self.is_grounded = True
        return self.x, self.y, self.angle


class PhysicsCharacterPuppet:
    """
    OverSimplified / History Matters style physics-aware character puppet.
    Features:
    - Modular body, head, hat/keffiyeh, and articulated limbs
    - Procedural squash & stretch based on movement velocity and reaction impulses
    - Dynamic eye rig (pupil gaze tracking, blinking, sweat drops, dollar eyes, knockout X eyes)
    - Speech mouth visemes synchronized to narration audio cadence
    """
    def __init__(self, character_id, base_sprites, anchor_pos=(960, 680), base_scale=1.0):
        self.character_id = character_id
        self.sprites = base_sprites  # Dictionary of PIL Images
        self.anchor_x, self.anchor_y = anchor_pos
        self.base_scale = base_scale

        # Physics springs
        self.bounce_spring = SpringDamper(stiffness=150.0, damping=12.0)
        self.squash_spring = SpringDamper(stiffness=180.0, damping=15.0)  # scale_y modifier
        self.tilt_spring = SpringDamper(stiffness=100.0, damping=10.0)    # head tilt angle
        self.arm_spring = SpringDamper(stiffness=130.0, damping=12.0)

        # Ragdoll simulation for knockout or dramatic falls
        self.ragdoll = RagdollEntity(self.anchor_x, self.anchor_y)
        self.is_ragdoll = False

        # Eye gaze & blink state
        self.blink_timer = 1.0  # Start with eyes fully open
        self.next_blink = random.uniform(2.5, 4.5)
        self.gaze_x = 0.0  # -1.0 to 1.0
        self.gaze_y = 0.0

        # Sweat drop animation
        self.sweat_progress = 0.0

    def trigger_reaction(self, reaction_type="shock"):
        """Triggers a physics impulse reaction."""
        if reaction_type == "shock":
            self.bounce_spring.impulse(-350.0)
            self.squash_spring.impulse(0.35)  # Stretch up
            self.tilt_spring.impulse(random.choice([-15.0, 15.0]))
        elif reaction_type == "faint":
            self.is_ragdoll = True
            self.ragdoll.x = self.anchor_x
            self.ragdoll.y = self.anchor_y
            self.ragdoll.launch(vx=random.uniform(-180, -260), vy=-300, torque=random.uniform(90, 140))
        elif reaction_type == "laugh":
            self.bounce_spring.impulse(200.0)
            self.squash_spring.impulse(-0.2)
        elif reaction_type == "reset":
            self.is_ragdoll = False
            self.bounce_spring.snap_to(0.0)
            self.squash_spring.snap_to(0.0)
            self.tilt_spring.snap_to(0.0)

    def update(self, dt, t_global, is_speaking=False, speech_rate=10.0):
        """Updates internal spring dynamics and procedural animation state."""
        if self.is_ragdoll:
            self.ragdoll.update(dt)
            return

        # UPGRADE 3: Continuous Alive Idle Breathing & Micro-Sway (prevents cardboard cutouts)
        self.idle_breath_scale = 1.0 + math.sin(t_global * 2.4) * 0.012
        self.idle_micro_sway = math.sin(t_global * 1.8) * 0.4

        # Idle breathing & subtle weight shift
        breath = math.sin(t_global * 2.8) * 4.0
        idle_tilt = math.sin(t_global * 1.5) * 1.5 + self.idle_micro_sway
        self.bounce_spring.target = breath
        self.tilt_spring.target = idle_tilt

        # Speech cadence modulation
        if is_speaking:
            speech_bob = abs(math.sin(t_global * speech_rate)) * 14.0
            self.bounce_spring.target -= speech_bob
            self.arm_spring.target = math.sin(t_global * (speech_rate * 0.5)) * 15.0
        else:
            self.arm_spring.target = 0.0

        self.bounce_spring.update(dt)
        self.squash_spring.update(dt)
        self.tilt_spring.update(dt)
        self.arm_spring.update(dt)

        # Blink timer
        self.blink_timer += dt
        if self.blink_timer >= self.next_blink:
            self.blink_timer = 0.0
            self.next_blink = random.uniform(2.5, 5.0)

    def render(self, canvas, t_rel, expression="neutral", action="idle", is_speaking=False, rim_light=None):
        """
        Renders the composite puppet with physics transformations onto the PIL canvas.
        Seamlessly supports unified character rigs (zero neck gap) and modular rigs.
        Includes automatic alpha-edge rim lighting when a light source is provided.
        """
        # 1. Check for Unified High-Fidelity Character Rig
        unified_img = self.sprites.get(self.character_id, None)

        if unified_img is not None:
            # Unified Rig Mode
            char_comp = unified_img.copy()
            cw, ch = char_comp.width, char_comp.height

            # Character Face Alignment Configuration (Exact 1:1 coordinates on 320x440 canvas)
            FACE_CONFIG = {
                "sheikh_zayed": {
                    "eye_center": (160, 144),
                    "eye_size": (72, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                },
                "sheikh_rashid": {
                    "eye_center": (160, 144),
                    "eye_size": (72, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                },
                "british_officer": {
                    "eye_center": (160, 146),
                    "eye_size": (72, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                },
                "worker": {
                    "eye_center": (160, 144),
                    "eye_size": (72, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                },
                "inventor": {
                    "eye_center": (160, 146),
                    "eye_size": (74, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                },
                "robot_minister": {
                    "eye_center": None,
                    "eye_size": None,
                    "mouth_center": (160, 240),
                    "mouth_size": (36, 16),
                },
                "j_robert_oppenheimer": {
                    "eye_center": (160, 145),
                    "eye_size": (72, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                },
                "harry_truman": {
                    "eye_center": (160, 146),
                    "eye_size": (72, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                },
                "emperor_hirohito": {
                    "eye_center": (160, 146),
                    "eye_size": (72, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                },
                "general_leslie_groves": {
                    "eye_center": (160, 144),
                    "eye_size": (72, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                },
                "colonel_paul_tibbets": {
                    "eye_center": (160, 145),
                    "eye_size": (72, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                },
                "general_korechika_anami": {
                    "eye_center": (160, 144),
                    "eye_size": (72, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                },
                "albert_einstein": {
                    "eye_center": (160, 145),
                    "eye_size": (72, 32),
                    "mouth_center": (160, 186),
                    "mouth_size": (42, 22),
                }
            }

            cfg = FACE_CONFIG.get(self.character_id, {
                "eye_center": (int(cw * 0.50), int(ch * 0.33)),
                "eye_size": (72, 32),
                "mouth_center": (int(cw * 0.50), int(ch * 0.42)),
                "mouth_size": (42, 22),
            })

            # Ragdoll knockout state
            if self.is_ragdoll:
                rx, ry, angle = self.ragdoll.x, self.ragdoll.y, self.ragdoll.angle
                x_eyes = self.sprites.get("eyes_x", None)
                if x_eyes and cfg["eye_center"]:
                    ex, ey = cfg["eye_center"]
                    ew, eh = cfg["eye_size"]
                    scaled_x = x_eyes.resize((ew, eh), Image.Resampling.BILINEAR)
                    char_comp.alpha_composite(scaled_x, (ex - ew // 2, ey - eh // 2))
                rotated = char_comp.rotate(-angle, resample=Image.Resampling.BILINEAR, expand=True)
                cx, cy = int(rx - rotated.width // 2), int(ry - rotated.height // 2)
                canvas.alpha_composite(rotated, (cx, cy))
                return

            # Eyes Selection
            if cfg["eye_center"]:
                is_blinking = (self.blink_timer < 0.16)
                if expression == "shocked":
                    eye_sprite = self.sprites.get("eyes_shocked")
                elif expression == "dollar":
                    eye_sprite = self.sprites.get("eyes_dollar")
                elif expression in ["x", "faint"]:
                    eye_sprite = self.sprites.get("eyes_x")
                elif is_blinking:
                    eye_sprite = self.sprites.get("eyes_blink")
                else:
                    eye_sprite = self.sprites.get("eyes_open")

                if eye_sprite:
                    ex, ey = cfg["eye_center"]
                    ew, eh = cfg["eye_size"]
                    g_x = int(self.gaze_x * 4)
                    g_y = int(self.gaze_y * 3)
                    scaled_eye = eye_sprite.resize((ew, eh), Image.Resampling.BILINEAR)
                    char_comp.alpha_composite(scaled_eye, (ex + g_x - ew // 2, ey + g_y - eh // 2))

            # Mouth Viseme Selection
            if self.character_id == "robot_minister":
                rdraw = ImageDraw.Draw(char_comp)
                if is_speaking:
                    wave_h = int((math.sin(t_rel * 25.0) + 1.0) * 5) + 3
                    rdraw.rectangle([146, 278 - wave_h, 174, 278 + wave_h], fill=(0, 242, 254, 255))
                    rdraw.line([(153, 278 - wave_h - 2), (153, 278 + wave_h + 2)], fill=(255, 255, 255, 255), width=2)
                    rdraw.line([(160, 278 - wave_h - 4), (160, 278 + wave_h + 4)], fill=(255, 255, 255, 255), width=2)
                    rdraw.line([(167, 278 - wave_h - 2), (167, 278 + wave_h + 2)], fill=(255, 255, 255, 255), width=2)
                else:
                    rdraw.rectangle([150, 277, 170, 279], fill=(0, 242, 254, 200))
            else:
                if is_speaking:
                    cycle = int(t_rel * 14) % 3
                    if cycle == 0:
                        mouth_sprite = self.sprites.get("mouth_open")
                    elif cycle == 1:
                        mouth_sprite = self.sprites.get("mouth_smile")
                    else:
                        mouth_sprite = self.sprites.get("mouth_closed")
                else:
                    mouth_sprite = self.sprites.get("mouth_smile" if expression == "happy" else "mouth_closed")

                if mouth_sprite:
                    mx, my = cfg["mouth_center"]
                    mw, mh = cfg["mouth_size"]
                    scaled_mouth = mouth_sprite.resize((mw, mh), Image.Resampling.BILINEAR)
                    char_comp.alpha_composite(scaled_mouth, (mx - mw // 2, my - mh // 2))

            # Sweat Drop for Shock
            if expression in ["shocked", "nervous"]:
                sdraw = ImageDraw.Draw(char_comp)
                sw_y = int(ch * 0.28 + (t_rel * 50) % 30)
                sw_x = int(cw * 0.32)
                sdraw.polygon([(sw_x, sw_y - 10), (sw_x - 5, sw_y + 3), (sw_x + 5, sw_y + 3)], fill=(120, 200, 255, 230))
                sdraw.ellipse([sw_x - 5, sw_y, sw_x + 5, sw_y + 8], fill=(120, 200, 255, 230))

            # Tilt Spring
            head_tilt = self.tilt_spring.pos
            if abs(head_tilt) > 0.4:
                char_comp = char_comp.rotate(head_tilt, resample=Image.Resampling.BILINEAR, expand=True)

            # Squash & Stretch with Continuous Idle Breathing Modulation
            breath_scale = getattr(self, "idle_breath_scale", 1.0)
            squash_y = (1.0 + self.squash_spring.pos) * breath_scale
            squash_x = 1.0 / max(0.5, squash_y)
            target_w = int(char_comp.width * self.base_scale * squash_x)
            target_h = int(char_comp.height * self.base_scale * squash_y)

            if target_w > 10 and target_h > 10:
                final_puppet = char_comp.resize((target_w, target_h), resample=Image.Resampling.BILINEAR)
            else:
                final_puppet = char_comp

            # Dynamic Alpha-Edge Character Rim Lighting (NumPy Fast Operation)
            if rim_light is not None:
                r_char_x = rim_light.get("char_x", self.anchor_x)
                r_light_x = rim_light.get("light_x", 960)
                r_col = rim_light.get("color", (251, 191, 36))
                r_op = rim_light.get("opacity", 0.75)
                r_shift = rim_light.get("shift_px", 5)
                final_puppet = apply_alpha_edge_rim_light(final_puppet, r_char_x, r_light_x, r_col, r_op, r_shift)

            # Ground Anchor & Bounce
            y_offset = self.bounce_spring.pos
            render_x = int(self.anchor_x - target_w // 2)
            render_y = int(self.anchor_y - target_h + y_offset)
            canvas.alpha_composite(final_puppet, (render_x, render_y))
            return

        # 2. Fallback Modular Head + Body Mode (with Zero-Gap Overlap Anchor)
        if self.is_ragdoll:
            rx, ry, angle = self.ragdoll.x, self.ragdoll.y, self.ragdoll.angle
            body_img = self.sprites.get(f"{self.character_id}_body", None)
            head_img = self.sprites.get(f"{self.character_id}_head", None)
            if not body_img or not head_img:
                return

            composite = Image.new("RGBA", (500, 700), (0, 0, 0, 0))
            composite.alpha_composite(body_img, (50, 180))
            composite.alpha_composite(head_img, (70, 80))  # Fixed snug anchor
            x_eyes = self.sprites.get("eyes_x", None)
            if x_eyes:
                composite.alpha_composite(x_eyes, (190, 170))

            rotated = composite.rotate(-angle, resample=Image.Resampling.BILINEAR, expand=True)
            cx, cy = int(rx - rotated.width // 2), int(ry - rotated.height // 2)
            canvas.alpha_composite(rotated, (cx, cy))
            return

        # Regular Modular Mode
        y_offset = self.bounce_spring.pos
        breath_scale = getattr(self, "idle_breath_scale", 1.0)
        squash_y = (1.0 + self.squash_spring.pos) * breath_scale
        squash_x = 1.0 / max(0.5, squash_y)

        head_tilt = self.tilt_spring.pos
        body_img = self.sprites.get(f"{self.character_id}_body")
        head_img = self.sprites.get(f"{self.character_id}_head")
        if not body_img or not head_img:
            return

        head_comp = head_img.copy()

        # Eyes
        is_blinking = (self.blink_timer < 0.16)
        if expression == "shocked":
            eye_sprite = self.sprites.get("eyes_shocked")
        elif expression == "dollar":
            eye_sprite = self.sprites.get("eyes_dollar")
        elif expression in ["x", "faint"]:
            eye_sprite = self.sprites.get("eyes_x")
        elif is_blinking:
            eye_sprite = self.sprites.get("eyes_blink")
        else:
            eye_sprite = self.sprites.get("eyes_open")

        if eye_sprite:
            eye_x = int(head_comp.width * 0.44 + self.gaze_x * 8)
            eye_y = int(head_comp.height * 0.43 + self.gaze_y * 5)
            head_comp.alpha_composite(eye_sprite, (eye_x - eye_sprite.width // 2, eye_y - eye_sprite.height // 2))

        # Mouth
        if is_speaking:
            cycle = int(t_rel * 14) % 3
            if cycle == 0:
                mouth_sprite = self.sprites.get("mouth_open")
            elif cycle == 1:
                mouth_sprite = self.sprites.get("mouth_smile")
            else:
                mouth_sprite = self.sprites.get("mouth_closed")
        else:
            mouth_sprite = self.sprites.get("mouth_smile" if expression == "happy" else "mouth_closed")

        if mouth_sprite:
            m_x = int(head_comp.width * 0.44)
            m_y = int(head_comp.height * 0.60)
            head_comp.alpha_composite(mouth_sprite, (m_x - mouth_sprite.width // 2, m_y - mouth_sprite.height // 2))

        if abs(head_tilt) > 0.5:
            head_comp = head_comp.rotate(head_tilt, resample=Image.Resampling.BILINEAR, expand=True)

        pw = max(body_img.width, head_comp.width) + 80
        ph = body_img.height + head_comp.height + 60
        puppet_canvas = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))

        # Snug overlap placement: collar connects directly to chin (NO GAP!)
        body_x = (pw - body_img.width) // 2
        body_y = int(head_comp.height * 0.55)
        puppet_canvas.alpha_composite(body_img, (body_x, body_y))

        head_x = (pw - head_comp.width) // 2
        head_y = 10
        puppet_canvas.alpha_composite(head_comp, (head_x, head_y))

        target_w = int(pw * self.base_scale * squash_x)
        target_h = int(ph * self.base_scale * squash_y)
        if target_w > 10 and target_h > 10:
            final_puppet = puppet_canvas.resize((target_w, target_h), resample=Image.Resampling.BILINEAR)
        else:
            final_puppet = puppet_canvas

        if rim_light is not None:
            r_char_x = rim_light.get("char_x", self.anchor_x)
            r_light_x = rim_light.get("light_x", 960)
            r_col = rim_light.get("color", (251, 191, 36))
            r_op = rim_light.get("opacity", 0.75)
            r_shift = rim_light.get("shift_px", 5)
            final_puppet = apply_alpha_edge_rim_light(final_puppet, r_char_x, r_light_x, r_col, r_op, r_shift)

        render_x = int(self.anchor_x - target_w // 2)
        render_y = int(self.anchor_y - target_h + y_offset)
        canvas.alpha_composite(final_puppet, (render_x, render_y))

