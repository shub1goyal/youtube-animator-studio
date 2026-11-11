"""
engine_2d/publisher/publish_to_youtube.py
Full-Auto YouTube Viral Publishing Orchestrator.
1. Synthesizes viral metadata (A/B Title, Chapter Markers, SEO Description, Tags, Pinned Comment)
2. Generates 1280x720 high-CTR thumbnail
3. Authenticates via YouTube Data API v3 OAuth2
4. Performs chunked resumable upload
5. Sets custom thumbnail & posts engagement-driving first comment
"""

import os
import sys
import json
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from youtube_auth import get_authenticated_service, test_channel_connection, discover_client_secret
from viral_metadata_engine import ViralMetadataEngine
from viral_thumbnail_generator import generate_high_ctr_thumbnail
from youtube_uploader import YouTubeUploader


def publish_episode(
    video_path,
    script_path=None,
    thumbnail_path=None,
    privacy="unlisted",
    title_variant="A",
    custom_title=None
):
    sys.stdout.reconfigure(line_buffering=True)
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file does not exist: {video_path}")

    # 1. Load Script Data
    script_data = {}
    if script_path and os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            script_data = json.load(f)
    elif os.path.exists(os.path.join("production", "directors_cut_script.json")):
        with open(os.path.join("production", "directors_cut_script.json"), "r", encoding="utf-8") as f:
            script_data = json.load(f)

    # 2. Generate Viral Metadata
    print("\n[Step 1/4] 🧠 Synthesizing Viral Metadata with 25-Yr Strategy Engine...", flush=True)
    meta_engine = ViralMetadataEngine(script_data=script_data)
    meta_pkg = meta_engine.generate_complete_viral_package()

    # Determine Title
    if custom_title:
        final_title = custom_title
    else:
        title_map = {"A": 0, "B": 1, "C": 2}
        idx = title_map.get(title_variant.upper(), 0)
        final_title = meta_pkg["title_options"][idx]["title"]

    description = meta_engine.generate_seo_description(final_title)
    tags = meta_pkg["tags"]
    pinned_comment = meta_pkg["pinned_comment"]

    # 3. Generate High-CTR Thumbnail
    if not thumbnail_path or not os.path.exists(thumbnail_path):
        print("\n[Step 2/4] 🖼️ Generating 1280x720 Broadcast CTR Thumbnail...", flush=True)
        thumb_out = os.path.join(os.path.dirname(video_path), "viral_youtube_thumbnail.jpg")
        generate_high_ctr_thumbnail(thumb_out)
        thumbnail_path = thumb_out
    else:
        print(f"\n[Step 2/4] 🖼️ Using provided thumbnail: {thumbnail_path}")

    # Save packaging report
    pkg_report_path = os.path.join(os.path.dirname(video_path), "YOUTUBE_PUBLISHING_PACKAGE.json")
    with open(pkg_report_path, "w", encoding="utf-8") as pf:
        json.dump({
            "video_path": os.path.abspath(video_path),
            "chosen_title": final_title,
            "title_options": meta_pkg["title_options"],
            "description": description,
            "tags": tags,
            "pinned_comment": pinned_comment,
            "thumbnail_path": os.path.abspath(thumbnail_path),
            "privacy_status": privacy
        }, pf, indent=2, ensure_ascii=False)
    print(f"📄 Saved YouTube Packaging Record: {pkg_report_path}")

    # 4. Upload to YouTube
    print("\n[Step 3/4] 🔑 Verifying YouTube OAuth2 Credentials...", flush=True)
    uploader = YouTubeUploader()

    print("\n[Step 4/4] 🚀 Uploading Video Stream to Channel...", flush=True)
    result = uploader.upload_video(
        video_path=video_path,
        title=final_title,
        description=description,
        tags=tags,
        thumbnail_path=thumbnail_path,
        pinned_comment=pinned_comment,
        category_id="27",
        privacy_status=privacy
    )

    print("\n" + "=" * 65)
    print("✨ EPISODE SUCCESSFULLY PUBLISHED TO YOUTUBE!")
    print(f"🎬 Watch URL:     {result['url']}")
    print(f"🛠️ Studio Editor: {result['studio_url']}")
    print("=" * 65)
    return result


def main():
    parser = argparse.ArgumentParser(description="Full-Auto YouTube Viral Video Publisher")
    parser.add_argument("--video", default=os.path.join("production", "master_animation.mp4"), help="Path to rendered MP4 video")
    parser.add_argument("--script", default=os.path.join("production", "directors_cut_script.json"), help="Path to script JSON")
    parser.add_argument("--thumbnail", default=None, help="Path to custom thumbnail JPEG")
    parser.add_argument("--privacy", choices=["unlisted", "public", "private"], default="unlisted", help="Upload privacy status")
    parser.add_argument("--variant", choices=["A", "B", "C"], default="A", help="Title variant to select")
    parser.add_argument("--title", default=None, help="Custom override title")
    parser.add_argument("--check-auth", action="store_true", help="Test YouTube OAuth connection without uploading")

    args = parser.parse_args()

    if args.check_auth:
        test_channel_connection()
        return

    publish_episode(
        video_path=args.video,
        script_path=args.script,
        thumbnail_path=args.thumbnail,
        privacy=args.privacy,
        title_variant=args.variant,
        custom_title=args.title
    )


if __name__ == "__main__":
    main()
