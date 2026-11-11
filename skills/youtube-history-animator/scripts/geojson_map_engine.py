"""
skills/youtube-history-animator/scripts/geojson_map_engine.py

Tactile Strategic Cartography Engine using Real-World Natural Earth GeoJSON Boundaries.
Renders broadcast-grade multi-country tactical map cutaways with geographic bounding boxes,
dark tactical ocean grid, glowing target country highlights, radar pings, and animated trajectory arrows.
"""

import os
import math
import json
import urllib.request
from pathlib import Path

GEOJSON_LOCAL_PATH = Path(__file__).resolve().parent / "assets" / "world_countries.geojson"
GEOJSON_URL = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"

REGION_PRESETS = {
    "cuba_missile": ["Cuba", "United States of America", "Russia"],
    "cold_war": ["Cuba", "United States of America", "Russia"],
    "europe": ["Germany", "France", "United Kingdom", "Poland", "Italy", "Spain", "Ukraine"],
    "ww2_europe": ["Germany", "United Kingdom", "France", "Russia", "Poland"],
    "india_subcontinent": ["India", "Pakistan", "Bangladesh"],
    "middle_east": ["United Arab Emirates", "Saudi Arabia", "Oman", "Iran"],
    "north_america": ["United States of America", "Canada", "Mexico"]
}

DEFAULT_CAPITALS = {
    "Cuba": (-82.3666, 23.1136, "HAVANA"),
    "United States of America": (-77.0369, 38.9072, "WASHINGTON D.C."),
    "Russia": (37.6173, 55.7558, "MOSCOW"),
    "United Kingdom": (-0.1278, 51.5074, "LONDON"),
    "France": (2.3522, 48.8566, "PARIS"),
    "Germany": (13.4050, 52.5200, "BERLIN"),
    "India": (77.2090, 28.6139, "NEW DELHI"),
    "United Arab Emirates": (54.3773, 24.4539, "ABU DHABI"),
    "Saudi Arabia": (46.6753, 24.7136, "RIYADH")
}


def ensure_geojson():
    """Ensures world_countries.geojson is cached locally."""
    if GEOJSON_LOCAL_PATH.is_file() and GEOJSON_LOCAL_PATH.stat().st_size > 100000:
        return True
    GEOJSON_LOCAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(GEOJSON_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            with open(GEOJSON_LOCAL_PATH, "wb") as f:
                f.write(data)
        return True
    except Exception as e:
        print(f"⚠️ GeoJSON download notice: {e}")
        return False


def load_world_geojson():
    """Loads and caches parsed GeoJSON feature list."""
    if ensure_geojson():
        try:
            with open(GEOJSON_LOCAL_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None


class GeoJsonMapEngine:
    """Renders authentic real-world tactical vector map cutaways for documentary scenes."""

    @classmethod
    def render_map_cutaway_svg(
        cls,
        region="cold_war",
        highlight_countries=None,
        highlight_color="#38bdf8",
        target_color="#ef4444",
        title="STRATEGIC THEATER OF OPERATIONS"
    ):
        """
        Builds a broadcast-grade 1920x1080 tactical SVG map with real coastlines,
        bounding-box projection, highlighted target nations, and radar sweeps.
        """
        geojson_data = load_world_geojson()

        # Determine target countries
        targets = []
        if highlight_countries:
            targets = highlight_countries
        elif region in REGION_PRESETS:
            targets = REGION_PRESETS[region]
        else:
            targets = ["United States of America", "Cuba"]

        # Default fallback if GeoJSON file unreadable
        if not geojson_data or "features" not in geojson_data:
            return cls._render_fallback_map(title)

        features = geojson_data["features"]

        # 1. Compute geographic bounding box across target countries
        target_coords = []
        target_features = []
        for feat in features:
            c_name = feat.get("properties", {}).get("name", "")
            if any(t.lower() == c_name.lower() or t.lower() in c_name.lower() for t in targets):
                target_features.append(feat)
                geom = feat.get("geometry", {})
                g_type = geom.get("type", "")
                coords = geom.get("coordinates", [])
                if g_type == "Polygon":
                    for ring in coords:
                        target_coords.extend(ring)
                elif g_type == "MultiPolygon":
                    for poly in coords:
                        for ring in poly:
                            target_coords.extend(ring)

        if not target_coords:
            # Fallback box around mid-Atlantic / Americas / Europe
            min_lon, max_lon = -100.0, 45.0
            min_lat, max_lat = 15.0, 65.0
        else:
            lons = [p[0] for p in target_coords]
            lats = [p[1] for p in target_coords]
            min_lon = max(-175.0, min(lons))
            max_lon = min(175.0, max(lons))
            min_lat = max(-60.0, min(lats))
            max_lat = min(78.0, max(lats))

        # Add 25% padding around bounding box
        lon_span = max(max_lon - min_lon, 30.0)
        lat_span = max(max_lat - min_lat, 20.0)
        pad_lon = lon_span * 0.22
        pad_lat = lat_span * 0.22

        min_lon -= pad_lon
        max_lon += pad_lon
        min_lat -= pad_lat
        max_lat += pad_lat

        center_lon = (min_lon + max_lon) / 2.0
        center_lat = (min_lat + max_lat) / 2.0
        lon_range = max_lon - min_lon
        lat_range = max_lat - min_lat

        # Canvas mapping (1920x1080 canvas with 80px margins)
        scale_x = 1760.0 / lon_range
        scale_y = 920.0 / lat_range
        scale = min(scale_x, scale_y)

        def project(lon, lat):
            x = 960.0 + (lon - center_lon) * scale
            y = 540.0 - (lat - center_lat) * scale
            return round(x, 1), round(y, 1)

        # 2. Render Base SVG Structure
        svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <style type="text/css">
      @keyframes radarPing {
        0% { r: 6px; opacity: 1; }
        100% { r: 38px; opacity: 0; }
      }
      @keyframes trajectoryDash {
        from { stroke-dashoffset: 400; }
        to { stroke-dashoffset: 0; }
      }
      .anim-ping { animation: radarPing 2.2s cubic-bezier(0, 0.2, 0.8, 1) infinite; }
      .anim-traj { animation: trajectoryDash 3.5s linear infinite; }
    </style>

    <filter id="map-radar-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="target-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <linearGradient id="mapOcean" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#071322"/>
      <stop offset="100%" stop-color="#030811"/>
    </linearGradient>
    <pattern id="tacticalGrid" width="60" height="60" patternUnits="userSpaceOnUse">
      <rect width="60" height="60" fill="none" stroke="#0f2942" stroke-width="0.8"/>
      <circle cx="30" cy="30" r="1.2" fill="#1e3a8a"/>
    </pattern>
  </defs>

  <!-- Deep Ocean Grid Background -->
  <rect width="1920" height="1080" fill="url(#mapOcean)"/>
  <rect width="1920" height="1080" fill="url(#tacticalGrid)" opacity="0.8"/>

  <!-- Compass Rose -->
  <g id="compass" transform="translate(1760, 160)" opacity="0.75">
    <circle cx="0" cy="0" r="48" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,4"/>
    <polygon points="0,-60 8,-16 0,0 -8,-16" fill="#38bdf8"/>
    <polygon points="0,60 8,16 0,0 -8,16" fill="#0369a1"/>
    <polygon points="60,0 16,8 0,0 16,-8" fill="#0369a1"/>
    <polygon points="-60,0 -16,8 0,0 -16,-8" fill="#0369a1"/>
    <text x="0" y="-68" font-family="Arial, sans-serif" font-size="12" fill="#38bdf8" font-weight="bold" text-anchor="middle">N</text>
  </g>

  <!-- Countries Layer -->
  <g id="countries-base">
"""

        # 3. Draw All Visible Countries
        target_name_set = {t.lower() for t in targets}
        highlighted_polys = []

        for feat in features:
            c_name = feat.get("properties", {}).get("name", "")
            is_target = any(t in c_name.lower() for t in target_name_set)
            geom = feat.get("geometry", {})
            g_type = geom.get("type", "")
            coords = geom.get("coordinates", [])

            rings = []
            if g_type == "Polygon":
                rings = coords
            elif g_type == "MultiPolygon":
                for poly in coords:
                    rings.extend(poly)

            for ring in rings:
                # Check if ring is roughly within bounding box
                r_lons = [p[0] for p in ring]
                r_lats = [p[1] for p in ring]
                if max(r_lons) < min_lon or min(r_lons) > max_lon or max(r_lats) < min_lat or min(r_lats) > max_lat:
                    continue

                pts = [project(p[0], p[1]) for p in ring]
                # Filter points outside screen & sub-pixel simplify for fast 60fps rendering
                simplified = []
                for p in pts:
                    if not (-200 <= p[0] <= 2120 and -200 <= p[1] <= 1280):
                        continue
                    if not simplified or (p[0] - simplified[-1][0])**2 + (p[1] - simplified[-1][1])**2 >= 4.0:
                        simplified.append(p)
                if len(simplified) < 3:
                    continue
                pts_str = " ".join([f"{x},{y}" for x, y in simplified])

                if is_target:
                    highlighted_polys.append((c_name, pts_str))
                else:
                    svg += f'    <polygon points="{pts_str}" fill="#172033" stroke="#334155" stroke-width="1.8" stroke-linejoin="round"/>\n'

        svg += '  </g>\n\n  <!-- Highlighted Target Nations -->\n  <g id="highlighted-nations">\n'

        # 4. Draw Highlighted Target Nations with Glow
        for c_name, pts_str in highlighted_polys:
            c_color = target_color if "cuba" in c_name.lower() or "russia" in c_name.lower() else highlight_color
            # Aura glow
            svg += f'    <polygon points="{pts_str}" fill="{c_color}" opacity="0.32" filter="url(#target-glow)"/>\n'
            # Solid boundary
            svg += f'    <polygon points="{pts_str}" fill="#1e293b" stroke="{c_color}" stroke-width="4.5" stroke-linejoin="round"/>\n'

        svg += '  </g>\n\n  <!-- Tactical Radar Rings & Trajectory -->\n  <g id="tactical-overlays">\n'

        # 5. Draw Capital Pins & Trajectory Arrows
        pin_coords = []
        for c_name in targets:
            match_key = None
            for k in DEFAULT_CAPITALS:
                if k.lower() in c_name.lower() or c_name.lower() in k.lower():
                    match_key = k
                    break
            if match_key:
                lon, lat, cap_name = DEFAULT_CAPITALS[match_key]
                px, py = project(lon, lat)
                if 40 <= px <= 1880 and 40 <= py <= 1040:
                    pin_coords.append((px, py, cap_name, match_key))
                    c_color = target_color if "cuba" in match_key.lower() or "russia" in match_key.lower() else highlight_color
                    # Radar pulse ring
                    svg += f'    <circle class="anim-ping" cx="{px}" cy="{py}" r="12" fill="none" stroke="{c_color}" stroke-width="2.5"/>\n'
                    # Solid center point
                    svg += f'    <circle cx="{px}" cy="{py}" r="6" fill="{c_color}" stroke="#ffffff" stroke-width="2"/>\n'
                    # Label pill
                    svg += f'    <rect x="{px - 60}" y="{py - 34}" width="120" height="22" rx="4" fill="#090d16" opacity="0.88" stroke="{c_color}" stroke-width="1.5"/>\n'
                    svg += f'    <text x="{px}" y="{py - 19}" font-family="Arial, sans-serif" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle" letter-spacing="1">{cap_name}</text>\n'

        # Trajectory Curved Arrow between targets (e.g. Havana -> Washington)
        if len(pin_coords) >= 2:
            p1 = pin_coords[0]
            p2 = pin_coords[1]
            mid_x = (p1[0] + p2[0]) / 2.0
            mid_y = (p1[1] + p2[1]) / 2.0 - 80.0
            svg += f'    <!-- Trajectory Missile Arc -->\n'
            svg += f'    <path class="anim-traj" d="M {p1[0]} {p1[1]} Q {mid_x} {mid_y} {p2[0]} {p2[1]}" fill="none" stroke="#ef4444" stroke-width="4.5" stroke-dasharray="12,6" filter="url(#map-radar-glow)"/>\n'

        svg += '  </g>\n\n'

        # 6. Title Header
        svg += f"""  <!-- Strategic Map Header -->
  <g id="map-header" transform="translate(60, 60)">
    <rect x="0" y="0" width="460" height="46" rx="6" fill="#070c16" opacity="0.92" stroke="#38bdf8" stroke-width="2.5"/>
    <circle cx="24" cy="23" r="6" fill="#ef4444"/>
    <text x="44" y="29" font-family="Arial, sans-serif" font-size="14" font-weight="900" fill="#38bdf8" letter-spacing="1.5">{title}</text>
  </g>
</svg>"""
        return svg

    @classmethod
    def _render_fallback_map(cls, title):
        """High-contrast tactical fallback if GeoJSON file is unavailable."""
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <rect width="1920" height="1080" fill="#071322"/>
  <text x="960" y="540" font-family="Arial" font-size="32" fill="#38bdf8" text-anchor="middle">{title}</text>
</svg>"""


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Real-World GeoJSON Tactical Map Engine")
    parser.add_argument("--region", default="cuba_missile", help="Region preset name")
    parser.add_argument("--title", default="STRATEGIC THEATER • OCTOBER 1962", help="Map Title")
    parser.add_argument("--color", default="#38bdf8", help="Highlight color")
    parser.add_argument("--out", default="tactical_map.svg", help="Output path")
    args = parser.parse_args()

    svg_content = GeoJsonMapEngine.render_map_cutaway_svg(
        region=args.region,
        highlight_color=args.color,
        title=args.title
    )
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"✅ Real-world tactical map generated: {args.out} ({len(svg_content)} bytes)")


if __name__ == "__main__":
    main()
