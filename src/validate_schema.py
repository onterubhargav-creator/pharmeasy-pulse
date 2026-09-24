from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
CLEAN = BASE / "data" / "pharmeasy_orders_clean.csv"
LOG_DIR = BASE / "logs"
LOG_DIR.mkdir(exist_ok=True)

def validate_schema(df, required_columns):
    missing = [c for c in required_columns if c not in df.columns]
    status = "blocked_schema" if missing else "validated"
    return {
        "status": status,
        "row_count": len(df),
        "missing_columns": missing
    }

REQUIRED = ["order_id", "region", "category", "product", "quantity", "sales_inr", "profit_inr"]

df = pd.read_csv(CLEAN)
print(f"Loaded: {len(df)} rows, columns: {list(df.columns)}")

# VALID case
result_valid = validate_schema(df, REQUIRED)
print("\nVALID CASE:")
print(result_valid)

# BLOCKED case - drop profit_inr
df_broken = df.drop(columns=["profit_inr"])
result_blocked = validate_schema(df_broken, REQUIRED)
print("\nBLOCKED CASE (profit_inr dropped):")
print(result_blocked)

# Save log for proof
with open(LOG_DIR / "schema_validation.log", "w") as f:
    f.write(f"VALID: {result_valid}\n")
    f.write(f"BLOCKED: {result_blocked}\n")

print("\nTask 1.3 DONE - log saved!")