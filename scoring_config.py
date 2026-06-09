"""
scoring_config.py — Single source of truth for SAS scoring methodology.

To change the scoring model:
  1. Edit the values in this file.
  2. Run: python generate_scoring_config.py
  3. Run: python rescore_v3.py  (or phase3_scoring.py)
  4. git add web/scoring_config.json web/ca_zip_scores.csv && git push

The web pages read scoring_config.json at runtime — no HTML edits needed.
"""

# ── Certification level definitions ──────────────────────────────────────────
# Each level maps drive-time thresholds (minutes, inclusive upper bound) to scores.
# Use 9999 as the catch-all for "beyond the last real threshold".

LEVELS = {
    "CSC": {
        "label":       "Comprehensive Stroke Center",
        "color":       "#c0392b",
        "scores":      {15: 100, 30: 85, 45: 65, 60: 50, 9999: 25},
    },
    "PSC": {
        "label":       "Primary Stroke Center",
        "color":       "#1d6fa4",
        "scores":      {15: 40, 30: 32, 45: 24, 60: 16, 9999: 8},
    },
    "ASRH": {
        "label":       "Acute Stroke Ready Hospital",
        "color":       "#6b7280",
        "scores":      {15: 25, 30: 20, 45: 15, 60: 10, 9999: 5},
    },
}

# ── Score tiers ───────────────────────────────────────────────────────────────
# "high" >= HIGH_THRESHOLD
# "medium" >= MEDIUM_THRESHOLD and < HIGH_THRESHOLD
# "low" < MEDIUM_THRESHOLD

TIERS = {
    "high":   {"min": 70,  "label": "Strong Access",   "color": "#1a7837"},
    "medium": {"min": 40,  "label": "Moderate Access",  "color": "#fec44f"},
    "low":    {"min": 0,   "label": "Limited Access",   "color": "#d7191c"},
}

# ── Color scale (used by sasColor() in map) ───────────────────────────────────
# Ordered low-to-high. Each band: [min_score, max_score_exclusive, hex_color, label]
COLOR_SCALE = [
    {"min": 0,  "max": 25,  "color": "#d7191c", "label": "Very Limited"},
    {"min": 25, "max": 41,  "color": "#f07b4f", "label": "Limited"},
    {"min": 41, "max": 56,  "color": "#fec44f", "label": "Moderate"},
    {"min": 56, "max": 71,  "color": "#a6d96a", "label": "Good"},
    {"min": 71, "max": 86,  "color": "#4dac26", "label": "Strong"},
    {"min": 86, "max": 101, "color": "#1a7837", "label": "Excellent"},
]

# ── Vulnerability flag thresholds ─────────────────────────────────────────────
FLAGS = {
    "socioeconomic_vulnerability": {
        "score_threshold":   40,    # score must be below this
        "poverty_threshold": 20.0,  # pct_below_poverty > this (OR uninsured)
        "uninsured_threshold": 15.0,
        "requires_majority_minority": True,
    },
    "clinical_risk": {
        "score_threshold":   40,
        "median_age_threshold": 40,
    },
    # double_jeopardy = both flags active simultaneously
}

# ── Drive time increment labels (for display only) ───────────────────────────
DRIVE_TIME_LABELS = ["0–15 min", "15–30 min", "30–45 min", "45–60 min", ">60 min"]

# ── Named scoring models ──────────────────────────────────────────────────────
# Each model defines its own level → drive-time → score table.
# "csv_column" is the column name written to ca_zip_scores.csv by rescore_v3.py.
# The web pages read this field from scoring_config.json to know which CSV column
# to use when that model is active (non-map pages; map.html re-scores dynamically).

MODELS = {
    "primary": {
        "name":        "Primary Model",
        "description": "CSC-weighted with 15-minute drive time increments.",
        "default":     True,
        "csv_column":  "sas_score",
        "levels": {
            "CSC": {15: 100, 30: 85, 45: 65, 60: 50, 9999: 25},
            "PSC": {15: 40,  30: 32, 45: 24, 60: 16, 9999: 8},
        },
    },
    "sensitivity": {
        "name":        "Sensitivity Model",
        "description": (
            "Research comparison — flat penalty structure. "
            "Two threshold penalties at 30 and 60 minutes. "
            "Use to isolate the effect of 15-minute increment scoring "
            "vs. two-threshold penalties."
        ),
        "default":     False,
        "csv_column":  "sas_score_sensitivity",
        "levels": {
            # CSC: base 100, −30 at >30 min → 70, −15 at >60 min → 55
            "CSC": {30: 100, 60: 70, 9999: 55},
            # PSC: base 50,  −15 at >30 min → 35, −15 at >60 min → 20
            "PSC": {30: 50,  60: 35, 9999: 20},
        },
    },
}

# ── Helper: score lookup ──────────────────────────────────────────────────────
def get_score(level: str, drive_minutes: float) -> int:
    """Return the SAS score for a given certification level and drive time.
    Uses the primary LEVELS table (backward-compatible).
    """
    if level not in LEVELS:
        return 0
    table = LEVELS[level]["scores"]
    for threshold in sorted(table.keys()):
        if drive_minutes <= threshold:
            return table[threshold]
    return 0


def get_model_score(model_id: str, level: str, drive_minutes: float) -> int:
    """Return the SAS score for a named model, certification level, and drive time."""
    model = MODELS.get(model_id)
    if not model:
        return 0
    table = model["levels"].get(level)
    if not table:
        return 0
    for threshold in sorted(table.keys()):
        if drive_minutes <= threshold:
            return table[threshold]
    return 0

def classify(score) -> str:
    """Return tier label for a score."""
    if score is None:
        return "unscored"
    for tier_name in ("high", "medium", "low"):
        if score >= TIERS[tier_name]["min"]:
            return tier_name
    return "low"

def sas_color(score) -> str:
    """Return the hex color for a score (mirrors sasColor() in JS)."""
    if score is None:
        return COLOR_SCALE[0]["color"]
    for band in COLOR_SCALE:
        if score < band["max"]:
            return band["color"]
    return COLOR_SCALE[-1]["color"]
