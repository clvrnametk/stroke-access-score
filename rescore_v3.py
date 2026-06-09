"""
rescore_v3.py
CSC-weighted scoring with 15-minute increments.
Clinical methodology: James Beavis RN BSN SCRN / Cedars-Sinai.
Uses web/ca_hospitals.json (LA County EMS-corrected) + data/drive_time_cache.json.
No API calls.

Scoring parameters are defined in scoring_config.py — edit there, not here.
"""
import json, csv, shutil
from datetime import datetime
from collections import Counter
import scoring_config as cfg

CACHE_PATH     = "data/drive_time_cache.json"
HOSPITALS_PATH = "web/ca_hospitals.json"
CSV_PATH       = "web/ca_zip_scores.csv"

# ── Scoring function ──────────────────────────────────────────────────────────
def calculate_sas(hospitals):
    """
    Score a ZIP code given a list of nearby hospitals with drive times.
    Returns (best_score, best_name, best_level, best_drive_minutes).
    Scoring parameters come from scoring_config.LEVELS.
    """
    best_score, best_name, best_level, best_drive = 0, None, None, None
    for h in hospitals:
        level = h.get('stroke_level', '')
        if level not in cfg.LEVELS:
            continue
        mins  = h.get('drive_minutes', 9999)
        score = cfg.get_score(level, mins)
        if score > best_score:
            best_score = score
            best_name  = h.get('facility_name', '')
            best_level = level
            best_drive = mins
    return best_score, best_name, best_level, best_drive


def tier(s):
    """Bucket label for summary table (not the same as SAS tiers)."""
    if s is None: return 'unscored'
    if s <= 24:   return '0-24'
    if s <= 49:   return '25-49'
    if s <= 74:   return '50-74'
    return '75-100'


# ── Load hospitals ────────────────────────────────────────────────────────────
print("Loading hospitals …")
with open(HOSPITALS_PATH) as f:
    hosp_list = json.load(f)

hosp_info  = {h['facility_id']: h for h in hosp_list}
level_counts = Counter(h.get('stroke_level', 'unknown') for h in hosp_list)
print(f"  {len(hosp_list)} hospitals  ({', '.join(f'{k}: {v}' for k,v in level_counts.items())})")

# ── Load drive time cache ─────────────────────────────────────────────────────
print("Loading drive time cache …")
with open(CACHE_PATH) as f:
    cache = json.load(f)

zip_hospitals = {}
for entry in cache.values():
    zcta = entry.get('zcta') or entry.get('zip_code', '')
    fid  = entry.get('facility_id') or entry.get('provider_id', '')
    mins = entry.get('drive_minutes', 9999)
    if not zcta or not fid:
        continue
    info = hosp_info.get(fid, {})
    zip_hospitals.setdefault(zcta, []).append({
        'facility_id':   fid,
        'facility_name': info.get('facility_name', fid),
        'stroke_level':  info.get('stroke_level', ''),
        'drive_minutes': mins,
    })

print(f"  {len(cache):,} cache entries  →  {len(zip_hospitals):,} ZIPs with drive times")

# ── Load existing CSV ─────────────────────────────────────────────────────────
print("Loading CSV …")
existing   = []
fieldnames = []
with open(CSV_PATH) as f:
    reader     = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    for row in reader:
        existing.append(row)

print(f"  {len(existing):,} rows, {len(fieldnames)} columns")

# Ensure sensitivity column exists in fieldnames (add after sas_score if missing)
if 'sas_score_sensitivity' not in fieldnames:
    idx = fieldnames.index('sas_score') + 1
    fieldnames.insert(idx, 'sas_score_sensitivity')
    print("  Added column: sas_score_sensitivity")

# ── Helper: safe float ────────────────────────────────────────────────────────
def sf(v, default=0.0):
    try:    return float(v) if v not in ('', None, 'None') else default
    except: return default

# ── Re-score ──────────────────────────────────────────────────────────────────
print("\nRe-scoring …")
before_tiers = Counter()
after_tiers  = Counter()
went_up = went_down = unchanged_count = 0
updated_rows = []

# Pull flag thresholds from config
sev_cfg = cfg.FLAGS["socioeconomic_vulnerability"]
crf_cfg = cfg.FLAGS["clinical_risk"]

for row in existing:
    zcta      = row['zcta']
    old_raw   = row.get('sas_score', '')
    old_score = None if old_raw in ('', 'None') else float(old_raw)
    before_tiers[tier(old_score)] += 1

    hospitals = zip_hospitals.get(zcta, [])
    new_score, best_name, best_level, best_drive = calculate_sas(hospitals)
    new_score = new_score if new_score > 0 else None

    # Recalculate flags using config thresholds
    s     = new_score if new_score is not None else 9999
    pov   = sf(row.get('pct_below_poverty'))
    unins = sf(row.get('pct_uninsured_adults_19_64'))
    age   = sf(row.get('median_age'))
    is_mm = int(sf(row.get('is_majority_minority', '0')))

    sev = int(
        s < sev_cfg["score_threshold"]
        and is_mm == 1
        and (pov > sev_cfg["poverty_threshold"] or unins > sev_cfg["uninsured_threshold"])
    )
    crf = int(s < crf_cfg["score_threshold"] and age > crf_cfg["median_age_threshold"])
    djf = int(sev == 1 and crf == 1)

    # Track changes
    if old_score == new_score:
        unchanged_count += 1
    elif new_score is not None and (old_score is None or new_score > old_score):
        went_up += 1
    else:
        went_down += 1

    after_tiers[tier(new_score)] += 1

    # ── Sensitivity model second pass ─────────────────────────────────────────
    # Uses cfg.MODELS["sensitivity"] levels — no flags recomputed (primary only).
    sens_model  = cfg.MODELS["sensitivity"]["levels"]
    sens_score  = 0
    for h in hospitals:
        level = h.get('stroke_level', '')
        if level not in sens_model:
            continue
        mins   = h.get('drive_minutes', 9999)
        table  = sens_model[level]
        for threshold in sorted(table.keys()):
            if mins <= threshold:
                s = table[threshold]
                break
        else:
            s = 0
        if s > sens_score:
            sens_score = s
    sens_score_out = sens_score if sens_score > 0 else None

    updated = dict(row)
    updated['sas_score']                        = '' if new_score is None else new_score
    updated['sas_score_sensitivity']            = '' if sens_score_out is None else sens_score_out
    updated['best_facility_name']               = best_name  or row.get('best_facility_name', '')
    updated['best_facility_type']               = best_level or row.get('best_facility_type', '')
    updated['socioeconomic_vulnerability_flag'] = sev
    updated['clinical_risk_flag']               = crf
    updated['double_jeopardy_flag']             = djf
    updated_rows.append(updated)

# ── Summary ───────────────────────────────────────────────────────────────────
total = len(existing)

print(f"\n{'='*58}")
print(f"  RESCORE SUMMARY  (v3 — CSC-weighted, 15-min increments)")
print(f"{'='*58}")
print(f"  Total ZIPs scored:  {total:,}")
print(f"  Scores changed:     {went_up + went_down:,}")
print(f"    ↑ Increased:      {went_up:,}")
print(f"    ↓ Decreased:      {went_down:,}")
print(f"    = Unchanged:      {unchanged_count:,}")

tiers_order = ['0-24','25-49','50-74','75-100','unscored']
print(f"\n  {'Tier':<12}  {'Before':>8}  {'After':>8}  {'Delta':>8}")
print(f"  {'-'*44}")
for t in tiers_order:
    b  = before_tiers[t]
    a  = after_tiers[t]
    d  = a - b
    ds = f'+{d}' if d > 0 else str(d) if d != 0 else '—'
    print(f"  {t:<12}  {b:>8,}  {a:>8,}  {ds:>8}")

scored_new = [float(r['sas_score']) for r in updated_rows if r['sas_score'] not in ('','None')]
if scored_new:
    scored_new.sort()
    n = len(scored_new)
    print(f"\n  New range:  {min(scored_new):.0f}–{max(scored_new):.0f}")
    print(f"  New mean:   {sum(scored_new)/n:.1f}")
    print(f"  New median: {scored_new[n//2]:.1f}")
print(f"{'='*58}")

# ── Back up and write ─────────────────────────────────────────────────────────
ts = datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy(CSV_PATH, f"data/ca_zip_scores_backup_{ts}.csv")
print(f"\n  Backup: data/ca_zip_scores_backup_{ts}.csv")

with open(CSV_PATH, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(updated_rows)

import os
print(f"  Written: {CSV_PATH}  ({os.path.getsize(CSV_PATH)//1024} KB, {len(updated_rows):,} rows)")
print("\nDone. No API calls were made.")
