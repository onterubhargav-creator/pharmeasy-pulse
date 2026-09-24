import pandas as pd
import numpy as np
import random
import os

N_UNIQUE = 2100
DUPES = 59
DATA = "../data"

# 16 raw variants only -> maps to 9 canonical (10th Kurnool zero orders)
RAW_VARIANTS = [
    "hyd", "Hyderabad",
    "mum", "Mumbai",
    "del", "Delhi",
    "chennai", "Madras",
    "kol", "Kolkata",
    "Pune",
    "Bengaluru", "blr", "bng",
    "Ahmedabad",
    "Jaipur"
] # len = 16

PRODUCTS = [("Dolo 650","Fever"), ("Azithral 500","Antibiotic"), ("Shelcal","Calcium"), ("Ecosprin","Cardiac"), ("Pan 40","Acidity"), ("Cetirizine","Allergy"), ("Metformin","Diabetes"), ("Atorva","Cholesterol")]

REGIONS_MASTER = ["Hyderabad","Mumbai","Delhi","Chennai","Kolkata","Pune","Bengaluru","Ahmedabad","Jaipur","Kurnool"]
STATE_OF = {r:"State" for r in REGIONS_MASTER}
TIER_OF = {r:("Tier1" if r in ["Hyderabad","Mumbai","Delhi","Bengaluru"] else "Tier2") for r in REGIONS_MASTER}
# Kurnool will be in master only

rows = []
base = []
oid = 1000

for i in range(N_UNIQUE):
    rc_raw = random.choice(RAW_VARIANTS)
    prod, cat = random.choice(PRODUCTS)
    qty = int(np.random.randint(1,11))
    sales = qty * int(np.random.randint(20,201))
    prof = f"{sales*0.2:.2f}"
    r = {"order_id":f"ORD{oid}","region":rc_raw,"category":cat,"product":prod,"quantity":qty,"sales_inr":sales,"profit_inr":prof,"order_value_inr":sales}
    rows.append(r.copy())
    base.append(r.copy())
    oid+=1

# Force guarantee all 9 active regions appear at least once (without adding new raw variants)
guarantee = ["Hyderabad","Mumbai","Delhi","chennai","Kolkata","Pune","Bengaluru","Ahmedabad","Jaipur"]
for i, g in enumerate(guarantee):
    rows[i]["region"] = g
    base[i]["region"] = g

# Inject EXACT missing counts after dedup stage
# 94 missing profit_inr
miss_prof_idx = np.random.choice(N_UNIQUE, 94, replace=False)
for idx in miss_prof_idx:
    rows[idx]["profit_inr"] = ""

# 48 missing category (non-overlapping)
remaining = [i for i in range(N_UNIQUE) if i not in miss_prof_idx]
miss_cat_idx = np.random.choice(remaining, 48, replace=False)
for idx in miss_cat_idx:
    rows[idx]["category"] = ""

# Add 59 exact duplicates - ONLY from non-missing rows to keep 94/48 intact
good_indices = [i for i in range(N_UNIQUE) if i not in miss_prof_idx and i not in miss_cat_idx]
for _ in range(DUPES):
    rows.append(base[random.choice(good_indices)].copy())

df_raw = pd.DataFrame(rows).sample(frac=1, random_state=2026).reset_index(drop=True)
os.makedirs(DATA, exist_ok=True)
df_raw.to_csv(DATA + "/pharmeasy_orders_raw.csv", index=False)
df_raw.to_csv("pharmeasy_orders_raw.csv", index=False)

df_master = pd.DataFrame([{"region":r,"state":STATE_OF[r],"tier":TIER_OF[r]} for r in REGIONS_MASTER])
df_master.to_csv(DATA + "/regions_master.csv", index=False)
df_master.to_csv("regions_master.csv", index=False)

print(f"Wrote pharmeasy_orders_raw.csv ({len(df_raw)} rows) and regions_master.csv ({len(df_master)} rows).")
print(f"Expected: Raw 2159, Unique 2100, Dupes 59, Missing profit 94, Missing cat 48, Region raw variants {df_raw['region'].nunique()}")