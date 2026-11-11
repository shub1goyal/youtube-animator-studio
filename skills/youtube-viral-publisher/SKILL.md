---
name: youtube-viral-publisher
description: >-
  Automates YouTube channel posting, viral packaging, and video optimization. Automatically detects client_secret_*.json from Downloads, authenticates via YouTube Data API v3 OAuth2, synthesizes high-CTR A/B titles, timestamped chapters, SEO descriptions, 500-char tags, high-CTR 1280x720 thumbnails, and engagement pinned comments, then performs chunked resumable 1080p uploads with automated thumbnail and comment injection.
---

# YouTube Viral Publisher & Autonomous Channel Manager

This skill completely automates the final step of YouTube content creation: **publishing, packaging, and optimizing finished animated documentaries and shorts for maximum algorithmic virality and click-through rates (CTR)**.

---

## 1. Quick One-Command Execution

### A. Publish Documentary Directly to YouTube:
Publishes the master video to your authenticated channel with high-CTR metadata, custom thumbnail, and pinned comment:
```powershell
py <plugin-root>/skills/youtube-viral-publisher\scripts\publish_to_youtube.py --video uae_12min_production\history_of_uae_13min_documentary.mp4 --privacy unlisted
```
*(Options for `--privacy`: `unlisted` for review, `public` for immediate launch, `private` for draft).*

### B. Verify YouTube Channel Connection:
Tests OAuth2 token and prints authenticated channel name, subscriber count, and total view stats:
```powershell
py <plugin-root>/skills/youtube-viral-publisher\scripts\publish_to_youtube.py --check-auth
```

### C. Select Title Variant for A/B Testing:
```powershell
# Variant A: Extreme Curiosity Gap (Default)
py <plugin-root>/skills/youtube-viral-publisher\scripts\publish_to_youtube.py --variant A

# Variant B: OverSimplified Comedic Style
py <plugin-root>/skills/youtube-viral-publisher\scripts\publish_to_youtube.py --variant B

# Variant C: High-Stakes Controversy
py <plugin-root>/skills/youtube-viral-publisher\scripts\publish_to_youtube.py --variant C
```

---

## 2. Autonomous Publishing Architecture

When invoked, the publisher executes 4 automated stages:

1. **OAuth2 Discovery & Lifecycle Management (`youtube_auth.py`)**:
   - Automatically scans `~/Downloads` for Google Cloud `client_secret_*.json`.
   - Caches client secrets securely in `~/.config/youtube/client_secret.json`.
   - Manages token persistence in `~/.config/youtube/youtube_token.json` with automatic token refresh on expiration (100% headless after initial 1-click browser consent).
2. **Viral Metadata & Chapter Synthesis (`viral_metadata_engine.py`)**:
   - **Calibrated Channel Branding**: Strictly tailored to **The Shadow Strategist (`@ShadowMindset_Hindi`)** with verified subscribe link (`https://www.youtube.com/@ShadowMindset_Hindi?sub_confirmation=1`) and channel manifesto (*"Duniya mein do tarah ke log hote hain: Ek wo jo control hote hain, aur dusre wo jo control karte hain"*).
   - **Titles**: 3 algorithmic variants engineered for 12%+ CTR ($\le 60-75$ characters) anchored in high-stakes curiosity, psychological warfare, and corporate/monopoly power plays.
   - **Description**: First 150 characters hook-dense; strategic masterstroke synopsis; exact timestamped chapters synced with audio wave boundaries; historical archive citations; official channel links; 6 targeted hashtags.
   - **Tags**: 500 characters combining authoritative channel tags (`the shadow strategist`, `shadow mindset hindi`, `power dynamics hindi`, `dark psychology hindi`, `strategy in hindi`) with topic-specific keywords.
   - **Pinned Comment**: High-velocity strategic engagement dilemma question designed to spark intense viewer debates and comment activity within the critical first 2 hours of upload.
3. **High-CTR Thumbnail Generation (`viral_thumbnail_generator.py`)**:
   - 1280x720 96% JPEG conforming to YouTube thumbnail standards.
   - OverSimplified Chibi character expressive reaction (shock/scheming).
   - High-contrast visual focal point (glistening pearl, crashing red arrow `-98%`, gold geyser).
   - Big 3D Bold Impact typography in golden yellow (`#FACC15`) with heavy black stroke and drop shadow.
4. **Resumable Chunked Uploader (`youtube_uploader.py`)**:
   - 10MB chunked resumable upload stream via YouTube Data API v3 (`videos.insert`).
   - Self-declares `containsSyntheticMedia = True` (satisfies YouTube 2024+ AI disclosure requirements).
   - Sets category to **Education (27)** or **Film & Animation (1)**.
   - Calls `thumbnails.set` to inject the custom high-CTR thumbnail.
   - Calls `commentThreads.insert` to post the pinned first comment.

---

## 3. Integration with Full-Auto Animation Studio

In `autonomous_studio.py`, add `--publish` flag to immediately push the finished documentary upon render:
```powershell
py <plugin-root>/skills/youtube-history-animator\scripts\full_auto_producer.py --topic "History of UAE" --format long_form --publish
```

---

## 4. YouTube Monetization & YPP Policy Compliance

The publisher ensures full compliance with YouTube Partner Program (YPP) guidelines:
- **Synthetic Media Disclosure**: Automatically flags video as containing AI synthetic narration/assets, preventing policy strikes.
- **Advertiser-Friendly (Green Dollar)**: Descriptions cite authentic public domain historical records (treaties of 1820, 1853, 1892) ensuring no reused/repetitious content penalties.
- **Copyright Safe**: Audio bed and vector assets are 100% procedurally synthesized or public domain.

