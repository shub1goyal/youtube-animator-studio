"""
skills/youtube-history-animator/scripts/vector_prop_library.py

Free 200,000+ Vector Prop Library with Iconify Open-Source API & Offline Parametric Fallback.
Fetches artist-drawn vector SVGs (prioritizing fluent-emoji-flat, noto, openmoji, game-icons),
caches locally in sprites/svg_cache/, and provides pristine procedural vector fallbacks.
"""

import os
import re
import json
import urllib.request
import urllib.parse
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent / "sprites" / "svg_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

PREFERRED_SETS = ["fluent-emoji-flat", "noto", "openmoji", "twemoji", "game-icons", "mdi"]

# Built-in high-quality procedural SVG fallbacks for core historical props
OFFLINE_PARAMETRIC_PROPS = {
    "telephone": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
      <ellipse cx="60" cy="98" rx="42" ry="12" fill="#020408" opacity="0.6"/>
      <path d="M 28 85 L 36 55 L 84 55 L 92 85 Z" fill="#b91c1c" stroke="#050608" stroke-width="4.5"/>
      <circle cx="60" cy="70" r="14" fill="#fef08a" stroke="#050608" stroke-width="3"/>
      <path d="M 16 45 C 16 32, 104 32, 104 45 C 90 40, 30 40, 16 45 Z" fill="#dc2626" stroke="#050608" stroke-width="4.5"/>
      <rect x="52" y="38" width="16" height="18" rx="4" fill="#991b1b" stroke="#050608" stroke-width="3"/>
    </svg>""",
    "hotline_phone": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
      <ellipse cx="60" cy="98" rx="42" ry="12" fill="#020408" opacity="0.6"/>
      <path d="M 28 85 L 36 55 L 84 55 L 92 85 Z" fill="#ef4444" stroke="#050608" stroke-width="4.5"/>
      <circle cx="60" cy="70" r="14" fill="#ffffff" stroke="#050608" stroke-width="3"/>
      <circle cx="60" cy="70" r="5" fill="#ef4444"/>
      <path d="M 16 45 C 16 30, 104 30, 104 45 C 90 38, 30 38, 16 45 Z" fill="#b91c1c" stroke="#050608" stroke-width="4.5"/>
    </svg>""",
    "map_folder": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
      <path d="M 20 40 L 45 40 L 55 50 L 100 50 L 100 90 L 20 90 Z" fill="#f59e0b" stroke="#050608" stroke-width="4.5" stroke-linejoin="round"/>
      <rect x="30" y="52" width="60" height="30" rx="3" fill="#fef3c7" stroke="#050608" stroke-width="2.5"/>
      <line x1="38" y1="62" x2="82" y2="62" stroke="#d97706" stroke-width="2.5"/>
      <line x1="38" y1="72" x2="70" y2="72" stroke="#d97706" stroke-width="2.5"/>
      <text x="60" y="80" font-family="Arial" font-size="10" font-weight="bold" fill="#dc2626" text-anchor="middle">TOP SECRET</text>
    </svg>""",
    "briefing_table": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 240" width="600" height="240">
      <!-- Ground Shadow -->
      <ellipse cx="300" cy="220" rx="280" ry="20" fill="#020408" opacity="0.75"/>
      <!-- Table Legs -->
      <rect x="70" y="110" width="28" height="105" fill="#1e293b" stroke="#050608" stroke-width="5"/>
      <rect x="502" y="110" width="28" height="105" fill="#1e293b" stroke="#050608" stroke-width="5"/>
      <!-- Heavy Solid Top Surface -->
      <polygon points="20,110 580,110 540,60 60,60" fill="#334155" stroke="#050608" stroke-width="6"/>
      <rect x="20" y="110" width="560" height="24" rx="4" fill="#1e293b" stroke="#050608" stroke-width="5"/>
      <!-- Strategic Map Pad in Center -->
      <polygon points="180,104 420,104 400,74 200,74" fill="#fef08a" stroke="#050608" stroke-width="3"/>
      <!-- Status Lights Panel on Rim -->
      <circle cx="80" cy="122" r="4.5" fill="#22c55e"/>
      <circle cx="100" cy="122" r="4.5" fill="#ef4444"/>
      <circle cx="120" cy="122" r="4.5" fill="#facc15"/>
    </svg>""",
    "microphone": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
      <ellipse cx="60" cy="105" rx="28" ry="8" fill="#020408" opacity="0.6"/>
      <line x1="60" y1="105" x2="60" y2="60" stroke="#050608" stroke-width="6"/>
      <rect x="46" y="25" width="28" height="42" rx="14" fill="#94a3b8" stroke="#050608" stroke-width="4.5"/>
      <line x1="46" y1="40" x2="74" y2="40" stroke="#050608" stroke-width="3"/>
      <line x1="46" y1="52" x2="74" y2="52" stroke="#050608" stroke-width="3"/>
    </svg>""",
    "treaty_scroll": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
      <path d="M 25 35 C 25 25, 45 25, 45 35 L 45 95 C 45 105, 25 105, 25 95 Z" fill="#fef3c7" stroke="#050608" stroke-width="4"/>
      <path d="M 35 30 L 95 30 L 95 90 L 35 90 Z" fill="#fef9c3" stroke="#050608" stroke-width="4"/>
      <circle cx="85" cy="80" r="9" fill="#dc2626" stroke="#050608" stroke-width="2.5"/>
      <line x1="45" y1="45" x2="85" y2="45" stroke="#92400e" stroke-width="2.5"/>
      <line x1="45" y1="58" x2="85" y2="58" stroke="#92400e" stroke-width="2.5"/>
    </svg>"""
}


class VectorPropLibrary:
    """Manages online fetching from Iconify and offline parametric vector props."""

    @classmethod
    def fetch_iconify_svg(cls, prefix, name):
        """Fetches raw SVG content from Iconify API."""
        url = f"https://api.iconify.design/{prefix}/{name}.svg"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                if resp.status == 200:
                    return resp.read().decode("utf-8")
        except Exception:
            pass
        return None

    @classmethod
    def search_iconify(cls, query, limit=10):
        """Searches Iconify API for icons matching query."""
        enc = urllib.parse.quote(query)
        url = f"https://api.iconify.design/search?query={enc}&limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    return data.get("icons", [])
        except Exception:
            pass
        return []

    @classmethod
    def get_prop_svg(cls, keyword, width=120, height=120):
        """
        Retrieves prop SVG string. Checks local cache first, then Iconify API,
        falling back to high-quality procedural vector SVG if offline.
        """
        clean_key = re.sub(r"[^a-zA-Z0-9_]", "_", keyword.lower()).strip("_")
        cache_file = CACHE_DIR / f"{clean_key}.svg"

        # 1. Local Cache Check
        if cache_file.is_file():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass

        # 2. Iconify API Search & Fetch
        icons = cls.search_iconify(keyword)
        if icons:
            # Sort by preferred sets
            def set_priority(icon_id):
                for idx, ps in enumerate(PREFERRED_SETS):
                    if icon_id.startswith(ps + ":") or icon_id.startswith(ps + "/"):
                        return idx
                return 99

            sorted_icons = sorted(icons, key=set_priority)
            for ic in sorted_icons:
                parts = ic.replace(":", "/").split("/")
                if len(parts) == 2:
                    svg_data = cls.fetch_iconify_svg(parts[0], parts[1])
                    if svg_data and "<svg" in svg_data:
                        # Write to cache
                        with open(cache_file, "w", encoding="utf-8") as f:
                            f.write(svg_data)
                        return svg_data

        # 3. Offline Parametric Fallback
        if clean_key in OFFLINE_PARAMETRIC_PROPS:
            fallback = OFFLINE_PARAMETRIC_PROPS[clean_key]
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(fallback)
            return fallback

        # Generic prop fallback
        generic_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
          <ellipse cx="{width//2}" cy="{height - 12}" rx="{width//3}" ry="8" fill="#020408" opacity="0.6"/>
          <rect x="{width//4}" y="{height//4}" width="{width//2}" height="{height//2}" rx="8" fill="#3b82f6" stroke="#050608" stroke-width="4"/>
          <text x="{width//2}" y="{height//2 + 5}" font-family="Arial" font-size="12" fill="#ffffff" font-weight="bold" text-anchor="middle">{clean_key.upper()[:8]}</text>
        </svg>"""
        return generic_svg


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Vector Prop Library & Iconify Fetcher")
    parser.add_argument("--prop", default="telephone", help="Prop keyword")
    parser.add_argument("--out", default="prop.svg", help="Output SVG path")
    args = parser.parse_args()

    svg_content = VectorPropLibrary.get_prop_svg(args.prop)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"✅ Prop SVG generated: {args.out} ({len(svg_content)} bytes)")


if __name__ == "__main__":
    main()

