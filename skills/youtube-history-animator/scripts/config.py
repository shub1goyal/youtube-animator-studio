"""
skills/youtube-history-animator/scripts/config.py
Central Configuration & Cross-Platform Path Portability Module.
Ensures zero hardcoded user paths and cross-platform binary resolution (Windows / Mac / Linux).
"""

import os
import sys
import shutil
from pathlib import Path

# Repository and scripts root
SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPTS_DIR.parent
PLUGIN_ROOT = SKILL_DIR.parent.parent


def get_gemini_api_keys():
    """
    Load Gemini API keys from environment variables or local gitignored api_keys.json.
    Priority:
    1. GEMINI_API_KEY (single key or comma-separated list)
    2. GEMINI_KEYS_PATH (path to json file)
    3. api_keys.json in current working directory, workspace root, or plugin root
    """
    keys = []
    
    # 1. Environment variable directly
    env_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_key:
        for k in env_key.split(","):
            k = k.strip()
            if k and k not in keys:
                keys.append(k)

    # 2. Custom JSON path
    custom_path = os.environ.get("GEMINI_KEYS_PATH", "").strip()
    candidate_paths = []
    if custom_path:
        candidate_paths.append(Path(custom_path))
    
    # Standard candidate locations for api_keys.json
    candidate_paths.extend([
        Path.cwd() / "api_keys.json",
        PLUGIN_ROOT / "api_keys.json",
        PLUGIN_ROOT.parent / "api_keys.json",
        Path.home() / ".config" / "gemini" / "api_keys.json",
    ])

    for p in candidate_paths:
        try:
            if p.is_file():
                import json
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        raw_list = data
                    elif isinstance(data, dict):
                        raw_list = data.get("gemini_api_keys", []) or data.get("keys", []) or data.get("api_keys", [])
                    else:
                        raw_list = []
                    for k in raw_list:
                        k_str = str(k).strip()
                        if k_str and k_str not in keys:
                            keys.append(k_str)
                if keys:
                    break
        except Exception:
            continue

    return keys


def find_ffmpeg_path():
    """
    Locate ffmpeg binary cross-platform.
    Checks:
    1. FFMPEG_PATH environment variable
    2. System PATH (shutil.which)
    3. Standard Windows Antigravity/winget/scoop/choco locations
    4. Standard Unix locations (/usr/local/bin, /usr/bin, /opt/homebrew/bin)
    """
    env_ffmpeg = os.environ.get("FFMPEG_PATH", "").strip()
    if env_ffmpeg and os.path.isfile(env_ffmpeg):
        return env_ffmpeg

    system_path = shutil.which("ffmpeg")
    if system_path:
        return system_path

    # Windows fallback search paths
    home = Path.home()
    local_app_data = os.environ.get("LOCALAPPDATA", str(home / "AppData" / "Local"))
    windows_candidates = [
        Path(local_app_data) / "agy" / "bin" / "ffmpeg.exe",
        Path(local_app_data) / "Microsoft" / "WinGet" / "Links" / "ffmpeg.exe",
        home / "scoop" / "shims" / "ffmpeg.exe",
        Path("C:/ProgramData/chocolatey/bin/ffmpeg.exe"),
        Path("C:/ffmpeg/bin/ffmpeg.exe"),
    ]
    for cand in windows_candidates:
        if cand.is_file():
            return str(cand)

    # Unix fallback search paths
    unix_candidates = [
        Path("/opt/homebrew/bin/ffmpeg"),
        Path("/usr/local/bin/ffmpeg"),
        Path("/usr/bin/ffmpeg"),
    ]
    for cand in unix_candidates:
        if cand.is_file():
            return str(cand)

    return "ffmpeg"


def find_ffprobe_path():
    """Locate ffprobe binary cross-platform."""
    ffmpeg = find_ffmpeg_path()
    if ffmpeg and ffmpeg != "ffmpeg":
        p = Path(ffmpeg)
        sibling = p.with_name("ffprobe.exe" if p.suffix == ".exe" else "ffprobe")
        if sibling.is_file():
            return str(sibling)
    
    probe = shutil.which("ffprobe")
    if probe:
        return probe
    return "ffprobe"


def find_chrome_path():
    """
    Locate Google Chrome or Chromium executable cross-platform.
    """
    env_chrome = os.environ.get("CHROME_PATH", "").strip()
    if env_chrome and os.path.isfile(env_chrome):
        return env_chrome

    for cmd in ["google-chrome", "chrome", "chromium", "google-chrome-stable", "brave"]:
        cand = shutil.which(cmd)
        if cand:
            return cand

    # Platform-specific paths
    home = Path.home()
    program_files = os.environ.get("PROGRAMFILES", "C:\\Program Files")
    program_files_x86 = os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")
    local_app_data = os.environ.get("LOCALAPPDATA", str(home / "AppData" / "Local"))

    candidates = [
        # Windows
        Path(program_files) / "Google" / "Chrome" / "Application" / "chrome.exe",
        Path(program_files_x86) / "Google" / "Chrome" / "Application" / "chrome.exe",
        Path(local_app_data) / "Google" / "Chrome" / "Application" / "chrome.exe",
        Path(program_files) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
        Path(program_files_x86) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
        # macOS
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        # Linux
        Path("/usr/bin/google-chrome"),
        Path("/usr/bin/chromium"),
        Path("/usr/bin/chromium-browser"),
    ]

    for cand in candidates:
        if cand.is_file():
            return str(cand)

    return "chrome"


# Export singleton constants
FFMPEG_PATH = find_ffmpeg_path()
FFPROBE_PATH = find_ffprobe_path()
CHROME_PATH = find_chrome_path()
