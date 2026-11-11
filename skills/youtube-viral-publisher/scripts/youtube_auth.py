"""
engine_2d/publisher/youtube_auth.py
YouTube Data API v3 OAuth 2.0 Authentication & Token Lifecycle Manager.
- Automatically discovers client_secret_*.json from Downloads or local configs.
- Handles browser-based local OAuth consent flow on port 0.
- Persists tokens for 100% headless, unattended future uploads.
- Auto-refreshes expired access tokens.
"""

import os
import sys
import json
import shutil
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

CONFIG_DIR = os.path.expanduser(r"~\.config\youtube")
TOKEN_PATH = os.path.join(CONFIG_DIR, "youtube_token.json")
DEFAULT_SECRET_PATH = os.path.join(CONFIG_DIR, "client_secret.json")


def discover_client_secret():
    """Finds client_secret_*.json in Downloads or config dir."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    # 1. Check existing copied client secret
    if os.path.exists(DEFAULT_SECRET_PATH) and os.path.getsize(DEFAULT_SECRET_PATH) > 50:
        return DEFAULT_SECRET_PATH

    # 2. Search in user Downloads folder
    downloads_dir = os.path.expanduser(r"~\Downloads")
    candidates = []
    if os.path.exists(downloads_dir):
        for f in os.listdir(downloads_dir):
            if f.startswith("client_secret_") and f.endswith(".json"):
                full_p = os.path.join(downloads_dir, f)
                try:
                    with open(full_p, "r", encoding="utf-8") as jf:
                        d = json.load(jf)
                        if "installed" in d or "web" in d:
                            mtime = os.path.getmtime(full_p)
                            candidates.append((mtime, full_p))
                except Exception:
                    pass

    if candidates:
        # Sort by newest
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_candidate = candidates[0][1]
        print(f"🔍 Discovered YouTube OAuth Client Secret in Downloads: {os.path.basename(best_candidate)}")
        shutil.copy2(best_candidate, DEFAULT_SECRET_PATH)
        print(f"📦 Stored client secret securely in: {DEFAULT_SECRET_PATH}")
        return DEFAULT_SECRET_PATH

    # 3. Check workspace directory
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.startswith("client_secret_") and f.endswith(".json"):
                full_p = os.path.abspath(os.path.join(root, f))
                shutil.copy2(full_p, DEFAULT_SECRET_PATH)
                return DEFAULT_SECRET_PATH

    return None


def get_authenticated_service(client_secret_path=None):
    """
    Authenticates with Google OAuth 2.0 and returns an authorized YouTube API v3 client.
    Handles token caching and automatic token refresh.
    """
    sys.stdout.reconfigure(line_buffering=True)
    os.makedirs(CONFIG_DIR, exist_ok=True)
    creds = None

    # 1. Load cached token if available
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            print(f"⚠️ Error loading cached token: {e}")
            creds = None

    # 2. Refresh or request new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired YouTube OAuth token...")
            try:
                creds.refresh(Request())
                print("✅ Token refreshed successfully.")
            except Exception as e:
                print(f"⚠️ Token refresh failed: {e}. Initiating re-authorization...")
                creds = None

        if not creds:
            secret_file = client_secret_path or discover_client_secret()
            if not secret_file or not os.path.exists(secret_file):
                raise FileNotFoundError(
                    f"❌ YouTube OAuth client_secret.json not found! "
                    f"Please place client_secret_*.json from Google Cloud Console into {CONFIG_DIR} or Downloads."
                )

            print(f"🔑 Authorizing YouTube Channel via Google OAuth 2.0 flow...", flush=True)
            print(f"👉 Opening browser window. Please sign into your YouTube channel and grant access.\n", flush=True)
            flow = InstalledAppFlow.from_client_secrets_file(secret_file, SCOPES)
            creds = flow.run_local_server(
                port=0,
                prompt="consent",
                authorization_prompt_message="🔗 YOUTUBE_AUTH_URL: {url}\n"
            )
            print("✅ Authorization granted!", flush=True)

        # Save credentials for future headless executions
        with open(TOKEN_PATH, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())
        print(f"💾 Persistent credentials cached in: {TOKEN_PATH}")

    # Build and return the YouTube service object
    youtube = build("youtube", "v3", credentials=creds)
    return youtube


def test_channel_connection():
    """Tests the connection and prints the authenticated channel details."""
    try:
        youtube = get_authenticated_service()
        response = youtube.channels().list(part="snippet,statistics", mine=True).execute()
        items = response.get("items", [])
        if not items:
            print("⚠️ Connected to YouTube, but no active channel found on this account.")
            return False

        channel = items[0]
        title = channel["snippet"]["title"]
        subs = channel["statistics"].get("subscriberCount", "Hidden")
        views = channel["statistics"].get("viewCount", "0")
        videos = channel["statistics"].get("videoCount", "0")
        custom_url = channel["snippet"].get("customUrl", "")

        print("\n" + "=" * 60)
        print("🎉 YOUTUBE CHANNEL CONNECTION VERIFIED")
        print("=" * 60)
        print(f"📺 Channel Name:      {title} ({custom_url})")
        print(f"👥 Subscribers:       {subs}")
        print(f"👀 Total Views:       {views}")
        print(f"🎬 Video Count:       {videos}")
        print("=" * 60 + "\n")
        return True
    except Exception as e:
        print(f"❌ YouTube connection check error: {e}")
        return False


if __name__ == "__main__":
    test_channel_connection()

