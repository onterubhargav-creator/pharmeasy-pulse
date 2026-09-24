import pandas as pd
import numpy as np
from pathlib import Path
import random

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)

np.random.seed(2026)
random.seed(2026)

REGIONS_ACTIVE = ["Hyderabad", "Warangal", "Vijayawada", "Visakhapatnam", "Guntur", "Nellore", "Tirupati", "Karimnagar", "Bengaluru"]
REGIONS_MASTER = REGIONS_ACTIVE + ["Kurnool"]
STATE_OF = {"Hyderabad":"Telangana","Warangal":"Telangana","Karimnagar":"Telangana","Vijayawada":"Andhra Pradesh","Visakhapatnam":"Andhra Pradesh","Guntur":"Andhra Pradesh","Nellore":"Andhra Pradesh","Tirupati":"Andhra Pradesh","Bengaluru":"Karnataka","Kurnool":"Andhra Pradesh"}
TIER_OF = {"Hyderabad":"Tier1","Bengaluru":"Tier1","Visakhapatnam":"Tier1","Vijayawada":"Tier2","Warangal":"Tier2","Guntur":"Tier2","Tirupati":"Tier2","Karimnagar":"Tier3","Nellore":"Tier3","Kurnool":"Tier3"}

# 16 raw variants -> 9 canonical (PROFESSOR CRITERIA)
RAW_VARIANTS = [
    "Hyderabad", "hyderabad ", "HYDERABAD",
    "Warangal", " warangal",
    "Vijayawada", "VIJAYAWADA",
    "Visakhapatnam", "visakhapatnam ",
    "Guntur", "GUNTUR ",
    "Nellore", " nellore",
    "Tirupati", "TIRUPATI",
    "Karimnagar",
    # Bengaluru will be canonical only to make total 16, adjust
]
# Ensure 16 only - let's fix exact 16
RAW_VARIANTS = RAW_VARIANTS[:16]

VARIANT_TO_CANON = {
    "Hyderabad":"Hyderabad", "hyderabad ":"Hyderabad", "HYDERABAD":"Hyderabad",
    "Warangal":"Warangal", " warangal":"Warangal",
    "Vijayawada":"Vijayawada", "VIJAYAWADA":"Vijayawada",
    "Visakhapatnam":"Visakhapatnam", "visakhapatnam ":"Visakhapatnam",
    "Guntur":"Guntur", "GUNTUR ":"Guntur",
    "Nellore":"Nellore", " nellore":"Nellore",
    "Tirupati":"Tirupati", "TIRUPATI":"Tirupati",
    "Karimnagar":"Karimnagar",
}

PRODUCTS = [("Paracetamol 500mg","Fever"),("Dolo 650","Fever"),("Azithromycin","Antibiotic"),("Vitamin D3","Supplements"),("Cetirizine","Cold"),("Sanitizer 100ml","Hygiene"),("Face Mask","Hygiene")]

N_UNIQUE = 2100
DUPES = 59 # PROFESSOR EXPECTS EXACTLY 59
TOTAL = N_UNIQUE + DUPES # 2159

rows = []
base = []
oid = 1000
for i in range(N_UNIQUE):
    rc_raw = random.choice(RAW_VARIANTS)
    prod, cat = random.choice(PRODUCTS)
    qty = np.random.randint(1,11)
    sales = qty * np.random.randint(20,201)
    prof = f"{sales*0.2:.2f}"
    r = {"order_id":f"ORD{oid}","region":rc_raw,"category":cat,"product":prod,"quantity":qty,"sales_inr":sales,"profit_inr":prof}
    rows.append(r.copy())
    base.append(r.copy())
    oid+=1

# Inject EXACT missing counts after dedup stage
# 94 missing profit_inr
miss_prof_idx = np.random.choice(N_UNIQUE, 94, replace=False)
for idx in miss_prof_idx:
    rows[idx]["profit_inr"] = ""

# 48 missing category (non-overlapping with profit missing for clarity)
remaining = [i for i in range(N_UNIQUE) if i not in miss_prof_idx]
miss_cat_idx = np.random.choice(remaining, 48, replace=False)
for idx in miss_cat_idx:
    rows[idx]["category"] = ""

# Add 59 exact duplicates
for _ in range(DUPES):
    rows.append(base[np.random.randint(0, N_UNIQUE)].copy())

df_raw = pd.DataFrame(rows).sample(frac=1, random_state=2026).reset_index(drop=True)
df_raw.to_csv(DATA / "pharmeasy_orders_raw.csv", index=False)
df_raw.to_csv("pharmeasy_orders_raw.csv", index=False)

df_master = pd.DataFrame([{"region":r,"state":STATE_OF[r],"tier":TIER_OF[r]} for r in REGIONS_MASTER])
df_master.to_csv(DATA / "regions_master.csv", index=False)
df_master.to_csv("regions_master.csv", index=False)

print(f"Wrote pharmeasy_orders_raw.csv ({len(df_raw)} rows) and regions_master.csv ({len(df_master)} rows).")
print(f"Expected: Raw 2159, Unique 2100, Dupes 59, Missing profit 94, Missing cat 48, Region raw variants {len(RAW_VARIANTS)}")