"""
engine_2d/motion_graphics.py
Motion Graphics & Kinetic Typography Engine.
Implements:
- Elastic Spring Overshoot Chapter Badges.
- High-Impact Rubber Stamp Slam with Camera Shake.
- Smooth Rapid Number Counters ($0 -> $500B).
- Stable, Broadcast-Paced Phrase-by-Phrase Kinetic Subtitles (No sliding jitter).
"""

import math
from PIL import Image, ImageDraw, ImageFont

FONT_TITLE = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_BODY = r"C:\Windows\Fonts\arialbd.ttf"


class MotionGraphicsEngine:
    def __init__(self):
        try:
            self.font_badge = ImageFont.truetype(FONT_TITLE, 26)
            self.font_title = ImageFont.truetype(FONT_TITLE, 52)
            self.font_stamp = ImageFont.truetype(FONT_TITLE, 64)
            self.font_counter = ImageFont.truetype(FONT_TITLE, 68)
            self.font_subtitle = ImageFont.truetype(FONT_BODY, 32)
            self.font_subtitle_active = ImageFont.truetype(FONT_BODY, 34)
        except OSError:
            self.font_badge = ImageFont.load_default()
            self.font_title = ImageFont.load_default()
            self.font_stamp = ImageFont.load_default()
            self.font_counter = ImageFont.load_default()
            self.font_subtitle = ImageFont.load_default()
            self.font_subtitle_active = ImageFont.load_default()

    def draw_chapter_badge(self, canvas, t_rel, chapter_text, accent=(241, 196, 15), pos=(60, 50)):
        """Draws top chapter badge with elastic drop-in easing."""
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        # Elastic drop in
        prog = min(1.0, t_rel / 0.6)
        overshoot = 1.0 - math.exp(-7.0 * prog) * math.cos(4.0 * math.pi * prog)
        y = int(-100 + (pos[1] - (-100)) * overshoot)
        
        # Measure text
        bbox = self.font_badge.getbbox(chapter_text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        pad_x, pad_y = 30, 14
        box = [pos[0], y, pos[0] + tw + pad_x * 2, y + th + pad_y * 2]
        
        # Dark pill with colored border
        draw.rounded_rectangle(box, radius=24, fill=(15, 23, 42, 220), outline=accent + (255,), width=3)
        draw.text((pos[0] + pad_x, y + pad_y - 2), chapter_text, font=self.font_badge, fill=accent + (255,))

    def draw_headline_card(self, canvas, t_rel, title, subtitle, pos=(60, 140)):
        """Draws main chapter headline card with fade & slide in."""
        if t_rel < 0.15:
            return
        draw = ImageDraw.Draw(canvas, "RGBA")
        prog = min(1.0, (t_rel - 0.15) / 0.5)
        # Ease out cubic
        ease = 1.0 - math.pow(1.0 - prog, 3)
        cur_x = int(-200 + (pos[0] - (-200)) * ease)
        alpha = int(255 * ease)
        
        # Shadow + Main text
        draw.text((cur_x + 3, pos[1] + 3), title, font=self.font_title, fill=(0, 0, 0, int(alpha * 0.7)))
        draw.text((cur_x, pos[1]), title, font=self.font_title, fill=(255, 255, 255, alpha))
        
        draw.text((cur_x + 2, pos[1] + 68 + 2), subtitle, font=self.font_subtitle, fill=(0, 0, 0, int(alpha * 0.6)))
        draw.text((cur_x, pos[1] + 68), subtitle, font=self.font_subtitle, fill=(209, 213, 219, alpha))

    def draw_slam_stamp(self, canvas, t_rel, text="CRASH: -95%", color=(239, 68, 68), center=(960, 480)):
        """Draws comic rubber stamp slamming down with impact and rotation."""
        if t_rel < 0.2:
            return
        draw = ImageDraw.Draw(canvas, "RGBA")
        
        prog = min(1.0, (t_rel - 0.2) / 0.25)
        scale = 3.0 - 2.0 * prog if prog < 1.0 else 1.0
        
        # Camera shake calculation
        shake = 0
        if 0.4 <= t_rel <= 0.8:
            dt = t_rel - 0.4
            shake = int(math.exp(-12.0 * dt) * math.sin(60.0 * dt) * 16.0)

        cx = center[0] + shake
        cy = center[1]
        
        bbox = self.font_stamp.getbbox(text)
        tw = int((bbox[2] - bbox[0]) * scale)
        th = int((bbox[3] - bbox[1]) * scale)
        
        sw, sh = tw + 80, th + 50
        stamp_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(stamp_img)
        
        sdraw.rounded_rectangle([10, 10, sw - 10, sh - 10], radius=14, outline=color + (255,), width=8)
        sdraw.text((35, 18), text, font=self.font_stamp, fill=color + (255,))
        
        rotated = stamp_img.rotate(-10.0, resample=Image.Resampling.BILINEAR, expand=True)
        canvas.alpha_composite(rotated, (cx - rotated.width // 2, cy - rotated.height // 2))

    def draw_number_counter(self, canvas, t_rel, start_val, end_val, prefix="$", suffix="", pos=(960, 420), color=(250, 204, 21)):
        """Animates a rapidly rolling numerical counter."""
        draw = ImageDraw.Draw(canvas, "RGBA")
        prog = min(1.0, t_rel / 2.5)
        ease = 1.0 - math.pow(1.0 - prog, 2)
        cur_val = int(start_val + (end_val - start_val) * ease)
        
        formatted_str = f"{prefix}{cur_val:,}{suffix}"
        bbox = self.font_counter.getbbox(formatted_str)
        tw = bbox[2] - bbox[0]
        
        cx = pos[0] - tw // 2
        cy = pos[1]
        
        draw.text((cx + 3, cy + 3), formatted_str, font=self.font_counter, fill=(0, 0, 0, 180))
        draw.text((cx, cy), formatted_str, font=self.font_counter, fill=color + (255,))

    def draw_kinetic_subtitle(self, canvas, t, full_text, duration_sec, center_x=960, bottom_y=1010, whisper_words=None):
        """
        Draws rock-solid, stable phrase-by-phrase subtitles.
        Text is segmented into calm 4-6 word semantic clauses.
        Uses exact Whisper word timestamps when available, or word-proportional distribution.
        The current active word highlights in vibrant gold without box jitter or pacing lag.
        """
        draw = ImageDraw.Draw(canvas, "RGBA")
        words = full_text.split()
        if not words:
            return

        # 1. Break text into fixed semantic phrases (punctuation or max 5 words)
        phrases = []
        cur_chunk = []
        for w in words:
            cur_chunk.append(w)
            if len(cur_chunk) >= 5 or w.endswith((',', '!', '?', '.')):
                phrases.append(cur_chunk)
                cur_chunk = []
        if cur_chunk:
            phrases.append(cur_chunk)

        n_phrases = len(phrases)
        if n_phrases == 0:
            return

        # 2. Determine active word and containing phrase with ZERO delay
        if whisper_words and len(whisper_words) > 0:
            # Find word in whisper_words matching time t
            active_w_idx = None
            for idx, item in enumerate(whisper_words):
                if item["start"] <= t <= item["end"]:
                    active_w_idx = idx
                    break
                elif item["start"] > t:
                    active_w_idx = max(0, idx - 1)
                    break
            if active_w_idx is None:
                active_w_idx = len(whisper_words) - 1 if t >= whisper_words[-1]["end"] else 0

            # Map whisper word index to full_text words proportionally
            frac = active_w_idx / max(1.0, float(len(whisper_words) - 1))
            global_word_idx = min(len(words) - 1, int(frac * len(words)))
        else:
            # Proportional word distribution (speech finishes ~0.3s before scene cut)
            speech_dur = max(0.5, duration_sec - 0.3)
            prog = min(1.0, max(0.0, t / speech_dur))
            global_word_idx = min(len(words) - 1, int(prog * len(words)))

        # Find which phrase contains global_word_idx
        word_count = 0
        active_phrase_idx = n_phrases - 1
        active_phrase = phrases[-1]
        active_word_in_phrase = len(phrases[-1]) - 1

        for p_idx, phrase in enumerate(phrases):
            if word_count + len(phrase) > global_word_idx:
                active_phrase_idx = p_idx
                active_phrase = phrase
                active_word_in_phrase = global_word_idx - word_count
                break
            word_count += len(phrase)

        # 3. Measure total width of the active phrase
        word_widths = []
        space_w = self.font_subtitle.getbbox(" ")[2] - self.font_subtitle.getbbox(" ")[0]
        total_phrase_w = 0

        for i, w in enumerate(active_phrase):
            font = self.font_subtitle_active if i == active_word_in_phrase else self.font_subtitle
            bbox = font.getbbox(w)
            w_w = bbox[2] - bbox[0]
            word_widths.append(w_w)
            total_phrase_w += w_w + (space_w if i < len(active_phrase) - 1 else 0)

        # 3. Draw static centered backdrop box
        pad_x, pad_y = 40, 18
        box_w = total_phrase_w + pad_x * 2
        box = [
            center_x - box_w // 2,
            bottom_y - 65,
            center_x + box_w // 2,
            bottom_y
        ]
        # High contrast charcoal pill with gold border
        draw.rounded_rectangle(box, radius=18, fill=(10, 15, 26, 235), outline=(250, 204, 21, 200), width=3)

        # 4. Render words inside stable box
        cur_x = center_x - box_w // 2 + pad_x
        y = bottom_y - 52

        for i, w in enumerate(active_phrase):
            is_active = (i == active_word_in_phrase)
            font = self.font_subtitle_active if is_active else self.font_subtitle
            color = (250, 204, 21, 255) if is_active else (255, 255, 255, 230)

            # Drop shadow for maximum readability
            draw.text((cur_x + 2, y + 2 - (3 if is_active else 0)), w, font=font, fill=(0, 0, 0, 200))
            draw.text((cur_x, y - (3 if is_active else 0)), w, font=font, fill=color)

            cur_x += word_widths[i] + space_w

    def draw_comic_alert(self, canvas, t_rel, badge_text="!!", head_pos=(960, 400), trigger_time=0.0, duration=1.8):
        """
        Draws MapLore-style comic exclamation badge (!! or ?!) popping above character's head
        with spring bounce physics on high-energy words.
        """
        if t_rel < trigger_time or t_rel > (trigger_time + duration):
            return
        
        elapsed = t_rel - trigger_time
        # Spring bounce pop-in: 0 -> 1.25 -> 1.0
        prog = min(1.0, elapsed / 0.35)
        scale = 1.0 - math.exp(-6.0 * prog) * math.cos(3.5 * math.pi * prog)
        if scale <= 0.01:
            return

        # Fade out in last 0.3s
        alpha = 255
        if elapsed > (duration - 0.3):
            alpha = int(255 * max(0.0, (duration - elapsed) / 0.3))

        target_x = head_pos[0]
        target_y = head_pos[1] - 95

        badge_w, badge_h = int(90 * scale), int(65 * scale)
        if badge_w < 10 or badge_h < 10:
            return

        badge_img = Image.new("RGBA", (badge_w + 30, badge_h + 30), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(badge_img)

        # Comic Jagged Starburst / Oval Badge
        bx0, by0 = 15, 15
        bx1, by1 = 15 + badge_w, 15 + badge_h

        # Red Drop Shadow Offset
        bdraw.rounded_rectangle([bx0 + 4, by0 + 4, bx1 + 4, by1 + 4], radius=16, fill=(239, 68, 68, int(alpha * 0.9)))
        # Yellow Fill with Black Ink Outline
        bdraw.rounded_rectangle([bx0, by0, bx1, by1], radius=16, fill=(250, 204, 21, alpha), outline=(5, 6, 8, alpha), width=5)

        # Draw Bold Badge Text (e.g. !! or ?!)
        try:
            alert_font = ImageFont.truetype(FONT_TITLE, max(12, int(38 * scale)))
        except OSError:
            alert_font = self.font_stamp

        bbox = alert_font.getbbox(badge_text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = bx0 + (badge_w - tw) // 2
        ty = by0 + (badge_h - th) // 2 - 3

        # Black Text with Red Drop Shadow
        bdraw.text((tx + 2, ty + 2), badge_text, font=alert_font, fill=(220, 38, 38, alpha))
        bdraw.text((tx, ty), badge_text, font=alert_font, fill=(5, 6, 8, alpha))

        # Paste onto canvas centered at target
        canvas.alpha_composite(badge_img, (target_x - badge_img.width // 2, target_y - badge_img.height // 2))

    def draw_curved_pointer_callout(self, canvas, t_rel, text="Wait... What?!", mouth_pos=(960, 480), trigger_time=0.0, duration=2.0, offset_x=120, offset_y=-110):
        """
        Draws MapLore-style curved-pointer micro-dialogue callout bubble
        with dashed pointer line extending to character's mouth.
        """
        if t_rel < trigger_time or t_rel > (trigger_time + duration):
            return

        elapsed = t_rel - trigger_time
        prog = min(1.0, elapsed / 0.28)
        scale = 1.0 - math.exp(-7.0 * prog) * math.cos(3.0 * math.pi * prog)
        if scale <= 0.01:
            return

        alpha = 255
        if elapsed > (duration - 0.35):
            alpha = int(255 * max(0.0, (duration - elapsed) / 0.35))

        draw = ImageDraw.Draw(canvas, "RGBA")

        # Bubble center position
        bx = int(mouth_pos[0] + offset_x)
        by = int(mouth_pos[1] + offset_y)

        # Measure text
        try:
            callout_font = ImageFont.truetype(FONT_TITLE, 28)
        except OSError:
            callout_font = self.font_subtitle

        bbox = callout_font.getbbox(text)
        tw = int((bbox[2] - bbox[0]) * scale)
        th = int((bbox[3] - bbox[1]) * scale)

        pad_x, pad_y = int(24 * scale), int(14 * scale)
        w_box = tw + pad_x * 2
        h_box = th + pad_y * 2

        x0 = bx - w_box // 2
        y0 = by - h_box // 2
        x1 = bx + w_box // 2
        y1 = by + h_box // 2

        # 1. Dashed curved pointer line from bubble edge to mouth_pos
        start_pt = (x0 + 15 if offset_x > 0 else x1 - 15, y1)
        mx, my = mouth_pos[0], mouth_pos[1]
        
        # Approximate Bezier curve with dotted segments
        num_dots = 8
        for k in range(num_dots):
            if k % 2 == 0:  # dashed pattern
                u1 = k / float(num_dots)
                u2 = (k + 0.8) / float(num_dots)
                # Quadratic Bezier
                ctrl_x = (start_pt[0] + mx) // 2 + (30 if offset_x > 0 else -30)
                ctrl_y = (start_pt[1] + my) // 2 + 10
                
                p1_x = int((1-u1)**2 * start_pt[0] + 2*(1-u1)*u1*ctrl_x + u1**2 * mx)
                p1_y = int((1-u1)**2 * start_pt[1] + 2*(1-u1)*u1*ctrl_y + u1**2 * my)
                p2_x = int((1-u2)**2 * start_pt[0] + 2*(1-u2)*u2*ctrl_x + u2**2 * mx)
                p2_y = int((1-u2)**2 * start_pt[1] + 2*(1-u2)*u2*ctrl_y + u2**2 * my)
                draw.line([(p1_x, p1_y), (p2_x, p2_y)], fill=(250, 204, 21, int(alpha * 0.9)), width=3)

        # 2. Dark Slate Pill with Gold Border & Drop Shadow
        draw.rounded_rectangle([x0 + 4, y0 + 4, x1 + 4, y1 + 4], radius=16, fill=(0, 0, 0, int(alpha * 0.6)))
        draw.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=(9, 13, 22, int(alpha * 0.94)), outline=(250, 204, 21, alpha), width=3)

        # 3. Text
        draw.text((x0 + pad_x, y0 + pad_y - 2), text, font=callout_font, fill=(255, 255, 255, alpha))

