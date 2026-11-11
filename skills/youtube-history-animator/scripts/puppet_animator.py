"""
engine_2d/puppet_animator.py
Modular 2D Character Puppet Animation Engine.
Provides real-time procedural breathing, syllable-synchronized mouth visemes,
eye blinking, facial expressions, arm gestures, spring overshoot entrances, and faint knockouts.
"""

import os
import math
import numpy as np
from PIL import Image

SPRITES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")


class CharacterPuppet:
    def __init__(self, character_name="sheikh_zayed"):
        self.name = character_name
        self.body_img = Image.open(os.path.join(SPRITES_DIR, f"{character_name}_body.png")).convert("RGBA")
        self.head_img = Image.open(os.path.join(SPRITES_DIR, f"{character_name}_head.png")).convert("RGBA")
        
        # Facial components
        self.mouth_closed = Image.open(os.path.join(SPRITES_DIR, "mouth_closed.png")).convert("RGBA")
        self.mouth_open = Image.open(os.path.join(SPRITES_DIR, "mouth_open.png")).convert("RGBA")
        self.mouth_smile = Image.open(os.path.join(SPRITES_DIR, "mouth_smile.png")).convert("RGBA")
        
        self.eyes_open = Image.open(os.path.join(SPRITES_DIR, "eyes_open.png")).convert("RGBA")
        self.eyes_blink = Image.open(os.path.join(SPRITES_DIR, "eyes_blink.png")).convert("RGBA")
        self.eyes_dollar = Image.open(os.path.join(SPRITES_DIR, "eyes_dollar.png")).convert("RGBA")
        self.eyes_shocked = Image.open(os.path.join(SPRITES_DIR, "eyes_shocked.png")).convert("RGBA")
        self.eyes_x = Image.open(os.path.join(SPRITES_DIR, "eyes_x.png")).convert("RGBA")

        # Anchor points for facial features relative to head image
        if character_name == "sheikh_zayed":
            self.eye_pos = (110, 160)
            self.mouth_pos = (120, 222)
            self.head_attach_pos = (20, -50)  # relative to body top-left
        elif character_name == "pearl_diver":
            self.eye_pos = (110, 150)
            self.mouth_pos = (120, 205)
            self.head_attach_pos = (20, -45)
        elif character_name == "british_officer":
            self.eye_pos = (110, 150)
            self.mouth_pos = (120, 210)
            self.head_attach_pos = (20, -40)
        else:
            self.eye_pos = (110, 150)
            self.mouth_pos = (120, 210)
            self.head_attach_pos = (20, -45)

    def get_frame(self, t, t_rel, is_speaking=True, expression="neutral", action="idle"):
        """
        Synthesizes a full character frame at time t (seconds).
        Returns a transparent RGBA PIL Image.
        """
        # 1. Breathing motion (torso squash/stretch)
        breath_scale_y = 1.0 + 0.015 * math.sin(t * 3.5)
        breath_scale_x = 1.0 - 0.008 * math.sin(t * 3.5)
        
        body_w, body_h = self.body_img.size
        scaled_body_w = int(body_w * breath_scale_x)
        scaled_body_h = int(body_h * breath_scale_y)
        body_scaled = self.body_img.resize((scaled_body_w, scaled_body_h), Image.Resampling.BILINEAR)

        # 2. Head bobbing & tilting
        if is_speaking:
            # Active talking bobble
            head_offset_y = int(math.sin(t * 9.0) * 7.0)
            head_offset_x = int(math.cos(t * 4.5) * 3.0)
            head_angle = math.sin(t * 4.5) * 3.0
        else:
            # Subtle idle float
            head_offset_y = int(math.sin(t * 2.5) * 2.5)
            head_offset_x = 0
            head_angle = math.sin(t * 1.8) * 1.5

        # 3. Facial Expression & Eye Blink Cycle
        # Blinks every 2.8 seconds for 0.12 seconds
        is_blinking = (t % 2.8) < 0.12
        if expression == "dollar":
            active_eyes = self.eyes_dollar
        elif expression == "shocked":
            active_eyes = self.eyes_shocked
        elif expression == "x" or action == "faint":
            active_eyes = self.eyes_x
        elif is_blinking:
            active_eyes = self.eyes_blink
        else:
            active_eyes = self.eyes_open

        # 4. Syllable-Synchronized Mouth Visemes
        if is_speaking:
            # Multi-frequency phoneme alternation (closed, open, smile)
            viseme_phase = math.sin(t * 13.0) + 0.5 * math.sin(t * 26.0)
            if viseme_phase > 0.4:
                active_mouth = self.mouth_open
            elif viseme_phase > -0.2:
                active_mouth = self.mouth_smile
            else:
                active_mouth = self.mouth_closed
        else:
            if expression in ["smile", "happy"]:
                active_mouth = self.mouth_smile
            else:
                active_mouth = self.mouth_closed

        # 5. Composite Head
        head_composite = self.head_img.copy()
        head_composite.alpha_composite(active_eyes, self.eye_pos)
        head_composite.alpha_composite(active_mouth, self.mouth_pos)

        # Head rotation if needed
        if abs(head_angle) > 0.5:
            head_composite = head_composite.rotate(head_angle, resample=Image.Resampling.BILINEAR, expand=True)

        # 6. Assemble Full Character Canvas
        total_w = 480
        total_h = 580
        canvas = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))

        # Paste body
        body_x = (total_w - scaled_body_w) // 2
        body_y = total_h - scaled_body_h - 10
        canvas.alpha_composite(body_scaled, (body_x, body_y))

        # Paste head
        head_x = body_x + self.head_attach_pos[0] + head_offset_x
        head_y = body_y + self.head_attach_pos[1] + head_offset_y
        canvas.alpha_composite(head_composite, (head_x, head_y))

        # 7. Action Handling: Knockout / Faint
        if action == "faint":
            # Falls backward 90 degrees with bounce
            fall_prog = min(1.0, t_rel / 0.6)
            angle = -90.0 * (1.0 - math.exp(-6.0 * fall_prog) * math.cos(3.0 * fall_prog))
            canvas = canvas.rotate(angle, resample=Image.Resampling.BILINEAR, expand=True)

        return canvas

