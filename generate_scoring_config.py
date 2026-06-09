"""
generate_scoring_config.py

Exports web/scoring_config.json from scoring_config.py.

Run this after any change to scoring_config.py, before pushing to Vercel.
The web pages fetch this file at runtime — no HTML edits needed.

Usage:
    python generate_scoring_config.py
"""
import json
import os
from datetime import datetime, timezone
import scoring_config as cfg

def build_penalty_table():
    """
    Build the human-readable penalty table used in about.html.
    Returns a list of rows: [{drive_time, level_scores: {CSC: n, PSC: n, ...}}]
    """
    # Collect all unique thresholds across all levels (excluding 9999)
    thresholds = sorted(set(
        t for lvl in cfg.LEVELS.values()
        for t in lvl["scores"].keys()
        if t != 9999
    ))

    rows = []
    prev = 0
    for t in thresholds:
        label = f"0–{t} min" if prev == 0 else f"{prev}–{t} min"
        row = {"drive_time": label, "scores": {}}
        for lvl_key, lvl_data in cfg.LEVELS.items():
            row["scores"][lvl_key] = cfg.get_score(lvl_key, t)
        rows.append(row)
        prev = t

    # Beyond last threshold row
    beyond_row = {"drive_time": f">{thresholds[-1]} min", "scores": {}}
    for lvl_key, lvl_data in cfg.LEVELS.items():
        beyond_row["scores"][lvl_key] = lvl_data["scores"][9999]
    rows.append(beyond_row)

    # No certified facility
    no_fac_row = {"drive_time": "No certified facility", "scores": {}}
    for lvl_key in cfg.LEVELS.keys():
        no_fac_row["scores"][lvl_key] = 0
    rows.append(no_fac_row)

    return rows


def build_models():
    """Serialize cfg.MODELS to JSON-safe format (int threshold keys → strings)."""
    out = {}
    for model_id, model in cfg.MODELS.items():
        out[model_id] = {
            "name":        model["name"],
            "description": model["description"],
            "default":     model["default"],
            "csv_column":  model["csv_column"],
            "levels": {
                level: {str(k): v for k, v in scores.items()}
                for level, scores in model["levels"].items()
            },
        }
    return out


def build_config():
    levels_out = {}
    for key, data in cfg.LEVELS.items():
        levels_out[key] = {
            "label": data["label"],
            "color": data["color"],
            # Convert int keys to strings for JSON
            "scores": {str(k): v for k, v in data["scores"].items()},
        }

    tiers_out = {k: dict(v) for k, v in cfg.TIERS.items()}

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "levels": levels_out,
        "tiers": tiers_out,
        "color_scale": cfg.COLOR_SCALE,
        "flags": cfg.FLAGS,
        "drive_time_labels": cfg.DRIVE_TIME_LABELS,
        "penalty_table": build_penalty_table(),
        "models": build_models(),
    }


if __name__ == "__main__":
    os.makedirs("web", exist_ok=True)
    config = build_config()
    out_path = "web/scoring_config.json"
    with open(out_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Wrote {out_path}")
    print(f"  Levels: {list(config['levels'].keys())}")
    print(f"  Tiers:  high>={config['tiers']['high']['min']}, medium>={config['tiers']['medium']['min']}")
    print(f"  Color scale bands: {len(config['color_scale'])}")
    print(f"  Penalty table rows: {len(config['penalty_table'])}")
    print(f"  Models: {list(config['models'].keys())}")
