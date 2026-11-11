"""
engine_2d/publisher/viral_metadata_engine.py
25-Year Veteran YouTube Algorithm & Virality Strategy Engine.
Generates:
1. High-CTR A/B/C Title Variants (Curiosity Gap, Irony, High Stakes)
2. SEO-Dominant Description with Timestamped Chapter Markers (Rich Search Snippets)
3. 500-Character Tag Cluster (Broad, Niche, and Competitor Intent)
4. Engagement-Driving Pinned First Comment
5. YouTube YPP Monetization Compliance & Synthetic Media Disclosures
"""

import os
import json
import re


class ViralMetadataEngine:
    """Produces YouTube packaging optimized for 12%+ CTR and maximum Average View Duration (AVD)."""

    def __init__(self, script_data=None, audio_dir=None):
        self.script_data = script_data or {}
        self.audio_dir = audio_dir
        self.topic = self.script_data.get("title", "History of UAE")
        self.scenes = self.script_data.get("scenes", [])

    def generate_viral_titles(self):
        """
        Generates 3 psychologically engineered titles for A/B testing:
        - Variant A: Extreme Curiosity Gap (High CTR)
        - Variant B: OverSimplified Comedic Framing (High Brand Recognition)
        - Variant C: High-Stakes Controversy / Historical Irony
        """
        topic = self.topic
        topic_lower = topic.lower()

        if any(k in topic_lower for k in ["uae", "emirates", "dubai", "abu dhabi"]):
            titles = [
                {
                    "variant": "A (Curiosity & Shock)",
                    "title": "How 1 Fake Pearl Almost Starved UAE... Before Finding $500B",
                    "char_count": 60,
                    "target_ctr": "13.5%",
                    "psychology": "Curiosity gap, contrast between extreme starvation and billions."
                },
                {
                    "variant": "B (OverSimplified Style)",
                    "title": "How UAE Turned Desert Sand into $500 Billion [Animated History]",
                    "char_count": 63,
                    "target_ctr": "12.8%",
                    "psychology": "Transformation hook, bracketed format tag, OverSimplified tone."
                },
                {
                    "variant": "C (High-Stakes Irony)",
                    "title": "The Forgotten Mistake That Created the Richest Nation on Earth",
                    "char_count": 62,
                    "target_ctr": "11.9%",
                    "psychology": "Superlative intrigue ('Richest Nation', 'Forgotten Mistake')."
                }
            ]
        else:
            titles = [
                {
                    "variant": "A (Extreme Curiosity)",
                    "title": f"The Dumbest Mistake in {topic} History",
                    "char_count": len(f"The Dumbest Mistake in {topic} History"),
                    "target_ctr": "12.5%",
                    "psychology": "Negative bias trigger, high curiosity gap."
                },
                {
                    "variant": "B (OverSimplified Style)",
                    "title": f"{topic} — OverSimplified [Full Animated Documentary]",
                    "char_count": len(f"{topic} — OverSimplified [Full Animated Documentary]"),
                    "target_ctr": "11.8%",
                    "psychology": "Format familiarity, high retention authority."
                },
                {
                    "variant": "C (High Stakes)",
                    "title": f"How One Secret Decision Changed {topic} Forever",
                    "char_count": len(f"How One Secret Decision Changed {topic} Forever"),
                    "target_ctr": "11.2%",
                    "psychology": "Conspiracy / secret knowledge hook."
                }
            ]
        return titles

    def generate_timestamped_chapters(self):
        """Generates exact YouTube chapter timestamps (e.g. 00:00 - Introduction)."""
        chapters = []
        cur_sec = 0.0

        for idx, sc in enumerate(self.scenes, 1):
            dur = float(sc.get("duration", 14.0))
            # Format to mm:ss
            mins = int(cur_sec // 60)
            secs = int(cur_sec % 60)
            ts_str = f"{mins:02d}:{secs:02d}"

            # Meaningful label from era badge or visual cue
            badge = sc.get("era_badge", "")
            if badge:
                label = badge.replace("•", "-").strip()
            else:
                label = f"Act {(idx-1)//5 + 1}: Scene {idx}"

            # Curate punchy chapter titles
            if idx == 1:
                label = "1930s Trucial Coast: Starving in the Desert"
            elif idx == 3:
                label = "Kokichi Mikimoto & The 1930 Pearl Crash"
            elif idx == 9:
                label = "1820: British Royal Navy & The Trucial Treaty"
            elif idx == 10:
                label = "1853: Perpetual Maritime Peace Accord"
            elif idx == 16:
                label = "1892: British Exclusive Hegemony"
            elif idx == 18:
                label = "1958: Abu Dhabi Strikes Black Gold!"
            elif idx == 21:
                label = "December 2, 1971: The Impossible UAE Union"
            elif idx == 28:
                label = "Smart Dubai: AI Ministers & The Space Age"
            elif idx == 38:
                label = "Engineering Burj Khalifa & Palm Jumeirah"
            elif idx == 48:
                label = "Emirates Mars Hope Mission & Grand Finale"

            # Filter duplicates or minor sub-scenes
            if idx in [1, 3, 6, 9, 10, 14, 16, 18, 21, 25, 28, 32, 38, 44, 48] or len(self.scenes) <= 10:
                chapters.append(f"{ts_str} - {label}")

            cur_sec += dur

        # Guarantee 00:00 start for YouTube chapter parsing
        if not chapters or not chapters[0].startswith("00:00"):
            chapters.insert(0, "00:00 - The Forgotten Trucial Coast")

        return "\n".join(chapters)

    def generate_seo_description(self, chosen_title=None):
        """Builds a broadcast-grade, retention-engineered YouTube description."""
        title = chosen_title or self.generate_viral_titles()[0]["title"]
        chapters = self.generate_timestamped_chapters()

        desc = f"""{title}

In 1930, the Trucial Coast was one of the poorest and harshest corners of the planet. Zero air conditioning, zero roads, and an entire population surviving on camel milk, dry dates, and dangerous deep-sea pearl diving. 

Then came the catastrophe: Japanese inventor Kokichi Mikimoto invented cultured pearls, and overnight, the Arabian Gulf's entire pearl market crashed by 98%. Families were pushed to the brink of starvation.

Fast forward less than a century: the UAE stands as a $500 billion global powerhouse, home to the world's tallest skyscraper, artificial island archipelagos, sovereign AI ministers, and space probes orbiting Mars. 

How did a cluster of Bedouin tribes survive British naval blockades, economic collapse, and desert wars to build the richest modern federation in history?

This is the complete, chaotic, and inspiring 13-minute animated history of the United Arab Emirates.

TIMESTAMPS:
{chapters}

SUBSCRIBE FOR MORE ANIMATED HISTORIES:
🔔 Turn on notifications so you never miss an episode!
👉 https://www.youtube.com/@HistoricalAnimations?sub_confirmation=1

CREDITS & HISTORICAL CITATIONS:
• UAE National Archives & Trucial States Historical Treaties (1820, 1853, 1892)
• Sheikh Zayed bin Sultan Al Nahyan: The Architect of the Union
• British Admiralty Records on the Persian Gulf Maritime Truces
• Animation style heavily inspired by OverSimplified and History Matters.

DISCLOSURE & AI TRANSPARENCY:
This educational animation combines procedural 2D ragdoll physics rigs, original vector art, and neural narration synthesized via Gemini Flash TTS (Voice: Charon) with historical forced-alignment synchronization.

#HistoryDocumentary #OverSimplified #UAEHistory #DubaiDocumentary #HistoryMatters #MiddleEastHistory
"""
        return desc.strip()

    def generate_seo_tags(self):
        """Generates 500 characters of high-volume and competitor SEO tags."""
        tags = [
            "history of uae",
            "dubai history documentary",
            "how uae became rich",
            "sheikh zayed history",
            "oversimplified",
            "oversimplified hindi",
            "history matters",
            "trucial states 1820",
            "pearl diving uae crash",
            "mikimoto cultured pearls",
            "oil discovered abu dhabi 1958",
            "uae union 1971",
            "sheikh rashid dubai vision",
            "burj khalifa engineering",
            "animated history documentary",
            "middle east history explained",
            "emirates mars mission hope",
            "dubai past vs present",
            "history documentary 2024",
            "history of dubai in hindi"
        ]
        tag_str = ", ".join(tags)
        # Ensure under 500 characters
        while len(tag_str) > 495:
            tags.pop()
            tag_str = ", ".join(tags)
        return tags

    def generate_pinned_comment(self):
        """Generates a high-conversion engagement pinned comment."""
        return (
            "🔥 PINNED QUESTION FOR THE COMMUNITY:\n\n"
            "Did you know that Japanese cultured pearls almost starved an entire nation before oil was ever discovered?\n\n"
            "Which era of UAE history surprised you the most: the 1820 British Royal Navy battles, or the 1971 alliance between Sheikh Zayed and Sheikh Rashid?\n\n"
            "👇 Drop your thoughts below! Best comment gets pinned & a heart! ❤️\n"
            "P.S. What historical topic should we animate next? Let us know!"
        )

    def generate_complete_viral_package(self):
        """Generates all viral assets as a structured dictionary."""
        titles = self.generate_viral_titles()
        selected_title = titles[0]["title"]
        desc = self.generate_seo_description(selected_title)
        tags = self.generate_seo_tags()
        pinned = self.generate_pinned_comment()
        chapters = self.generate_timestamped_chapters()

        package = {
            "title_options": titles,
            "selected_title": selected_title,
            "description": desc,
            "tags": tags,
            "pinned_comment": pinned,
            "chapters": chapters,
            "category_id": "27",  # Education
            "privacy_status": "unlisted",  # Safe default
            "self_declared_made_for_kids": False,
            "contains_synthetic_media": True
        }
        return package


if __name__ == "__main__":
    engine = ViralMetadataEngine()
    pkg = engine.generate_complete_viral_package()
    print("=" * 60)
    print(f"🎬 SELECTED TITLE: {pkg['selected_title']}")
    print("=" * 60)
    print(f"🏷️ TAGS ({len(', '.join(pkg['tags']))} chars): {', '.join(pkg['tags'])}\n")
    print(f"📌 PINNED COMMENT:\n{pkg['pinned_comment']}\n")
    print("=" * 60)
