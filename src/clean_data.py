import pandas as pd
import os

RAW_PATH = "../data/pharmeasy_orders_raw.csv"
CLEAN_PATH = "../data/pharmeasy_orders_clean.csv"
REGIONS_MASTER = "../data/regions_master.csv"

df = pd.read_csv(RAW_PATH)
print(f"Raw: {len(df)} rows")

# STEP 1: Dedup by order_id keep last
before = len(df)
df = df.drop_duplicates(subset=['order_id'], keep='last')
print(f"After dedup: {len(df)}")

print(f"Missing profit_inr: {df['profit_inr'].isna().sum()}")
print(f"Missing category: {df['category'].isna().sum() + (df['category']=='').sum()}")
print(f"Region variants raw: {df['region'].nunique()}")

# STEP 2: Region -> 9 canonical - SUPER ROBUST
CANONICAL_9 = ["Hyderabad","Mumbai","Delhi","Chennai","Kolkata","Pune","Bengaluru","Ahmedabad","Jaipur"]

def clean_region(r):
    r_low = str(r).strip().lower()
    if 'hyd' in r_low:
        return 'Hyderabad'
    if 'mum' in r_low or 'bomb' in r_low:
        return 'Mumbai'
    if 'del' in r_low:
        return 'Delhi'
    if 'chen' in r_low or 'madr' in r_low:
        return 'Chennai'
    if 'kol' in r_low or 'calc' in r_low:
        return 'Kolkata'
    if 'pune' in r_low or 'poona' in r_low:
        return 'Pune'
    if 'beng' in r_low or 'bang' in r_low or 'blr' in r_low or 'bng' in r_low:
        return 'Bengaluru'
    if 'ahme' in r_low or 'ahmd' in r_low:
        return 'Ahmedabad'
    if 'jaip' in r_low or 'jpr' in r_low:
        return 'Jaipur'
    # fallback - force to one of 9 to avoid extra canonical
    return 'Hyderabad'

df['region'] = df['region'].apply(clean_region)

# STEP 3: Category impute - 48 rows (product lookup)
product_cat_map = df.dropna(subset=['category']).drop_duplicates('product')[['product','category']].set_index('product')['category'].to_dict()
if not product_cat_map and 'product_name' in df.columns:
    product_cat_map = df.dropna(subset=['category']).drop_duplicates('product_name').set_index('product_name')['category'].to_dict()
    df['category'] = df.apply(lambda r: product_cat_map.get(r['product_name']) if pd.isna(r['category']) or r['category']=='' else r['category'], axis=1)
else:
    df['category'] = df['category'].replace('', pd.NA).fillna(df['product'].map(product_cat_map))

# STEP 4: Profit Impute - 94 rows (category mean margin method)
if 'sales_inr' in df.columns and 'order_value_inr' not in df.columns:
    df['order_value_inr'] = df['sales_inr']

df['margin'] = df['profit_inr'] / df['order_value_inr']
cat_margin = df.groupby('category')['margin'].mean()
overall_margin = df['margin'].mean()

def fill_profit(row):
    if pd.notna(row['profit_inr']):
        return row['profit_inr']
    m = cat_margin.get(row['category'], overall_margin)
    return row['order_value_inr'] * m

df['profit_inr'] = df.apply(fill_profit, axis=1)
df = df.drop(columns=['margin'])

# Final save
os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
df.to_csv(CLEAN_PATH, index=False)
print(f"clean saved: {len(df)} rows, columns: {list(df.columns)}")
print(f"Saved to {os.path.abspath(CLEAN_PATH)}")
print(f"Final Region canonical: {df['region'].nunique()} - {sorted(df['region'].unique())}")