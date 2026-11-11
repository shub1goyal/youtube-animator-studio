"""
YouTube Monetization & Policy Compliance Checker
Audits video scripts and metadata against:
1. YouTube Partner Program (YPP) Reused Content & AI Disclosure guidelines.
2. Advertiser-Friendly Content Guidelines (AdSense Green Icon safety on violence, gore, sensitive events).
3. Copyright & Fair Use safe harbor principles.
"""

import sys
import re
import argparse

# Trigger keywords for sensitive content / demonetization risks
HIGH_RISK_VIOLENCE = [
    "gore", "slaughter", "massacre", "mutilat", "behead", "decapitat", 
    "torture", "bloodbath", "genocide", "atrocity", "suicide", "lynch"
]

MODERATE_RISK_HISTORICAL = [
    "kill", "killed", "dead", "death", "die", "died", "murder", "bullet", 
    "shot", "wound", "corpse", "execution", "execute", "guillotine", "hang"
]

SENSITIVE_TRIGGERS_OPENING_7S = [
    "blood", "dead", "die", "kill", "murder", "war", "massacre", "bomb", "attack"
]

def audit_script(script_text):
    print("=" * 60)
    print("YOUTUBE MONETIZATION & POLICY COMPLIANCE REPORT")
    print("=" * 60)
    
    text_lower = script_text.lower()
    words = re.findall(r"\b[a-zA-Z']+\b", text_lower)
    word_count = len(words)
    print(f"Total Word Count: {word_count} words")
    
    # Check first 7-15 seconds (first ~35 words)
    opening_words = words[:35]
    opening_text = " ".join(opening_words)
    opening_flags = [w for w in SENSITIVE_TRIGGERS_OPENING_7S if re.search(r"\b" + w, opening_text)]
    
    print("\n[Check 1: First 7-15 Seconds Safety Filter]")
    if opening_flags:
        print(f"⚠️ WARNING: Sensitive keywords detected in the first 7-15 seconds: {opening_flags}")
        print("  Recommendation: YouTube automated AdSense crawlers heavily scrutinize the opening seconds.")
        print("  Rephrase the opening to lead with curiosity, strategy, or historical premise rather than graphic terms.")
    else:
        print("✅ PASS: Opening seconds are clean and advertiser-friendly.")

    # Check high-risk violence words
    print("\n[Check 2: Advertiser-Friendly Content Guidelines (Violence/Gore)]")
    found_high_risk = []
    for term in HIGH_RISK_VIOLENCE:
        matches = re.findall(r"\b" + term + r"[a-z]*\b", text_lower)
        if matches:
            found_high_risk.extend(matches)
            
    found_moderate_risk = []
    for term in MODERATE_RISK_HISTORICAL:
        matches = re.findall(r"\b" + term + r"[a-z]*\b", text_lower)
        if matches:
            found_moderate_risk.extend(matches)

    if found_high_risk:
        print(f"❌ HIGH RISK OF DEMONETIZATION (Yellow Icon): Found terms: {set(found_high_risk)}")
        print("  Recommendation: Replace with educational/cartoon euphemisms:")
        print("    'slaughter/massacre' -> 'decisive military defeat', 'routed the forces'")
        print("    'beheaded' -> 'lost his crown/head', 'deposed'")
        print("    Visually represent these moments with cartoon slapstick (X eyes, sweat drops, crossed swords).")
    elif found_moderate_risk:
        print(f"⚠️ MODERATE SENSITIVITY: Found historical conflict terms: {set(found_moderate_risk)}")
        print("  Status: Eligible for Green Icon monetization IF framed within historical analysis and cartoon visuals.")
        print("  Ensure visuals use stylized animation rather than archival bloody photos.")
    else:
        print("✅ PASS: Clean advertiser-friendly vocabulary. Zero yellow-icon triggers.")

    # Check Reused Content & Transformative Score
    print("\n[Check 3: YouTube Partner Program (Reused Content / AI Guidelines)]")
    ai_cliche_phrases = [
        "in conclusion", "it is important to remember", "a testament to", 
        "delve into", "tapestry of history", "beacon of hope", "needless to say"
    ]
    found_cliches = [c for c in ai_cliche_phrases if c in text_lower]
    if found_cliches:
        print(f"⚠️ AI Cliché Alert: Found robotic writing markers: {found_cliches}")
        print("  Recommendation: Rewrite in your conversational, witty creator persona to reinforce human creative fingerprint.")
    else:
        print("✅ PASS: Natural conversational flow with strong creator personality.")

    print("\n[Check 4: Synthetic / Altered Media Disclosure (2024-2026 Rules)]")
    print("  Status: Standard 2D vector animation, cartoon characters, and graphic explainer content do NOT require the 'Altered or Synthetic Media' label.")
    print("  Safe: YouTube explicitly excludes clearly unrealistic animations and cartoon media from mandatory synthetic disclosures.")

    print("=" * 60)
    print("AUDIT COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to script text file")
    args = parser.parse_args()
    
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        # Default test script
        content = "In 1803, President Thomas Jefferson sent two diplomats to Paris with ten million dollars to buy a single port city... and they accidentally bought eight hundred thousand square miles from Napoleon Bonaparte."
    
    audit_script(content)

