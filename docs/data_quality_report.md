# Task 1.4 - Data Quality Report - PharmEasy Pulse

## Dataset Summary
- Raw rows: 2159
- Clean rows: 1714
- Removed: 445 rows
- Final Columns: order_id, order_date, region, category, product, quantity, sales_inr, profit_inr

## Task 1.2 Fixes -> Data Quality Dimension Mapping

1. **Removing exact duplicates**
   - Dimension: Uniqueness
   - Fix: df.drop_duplicates()

2. **Normalizing region text (e.g., 'south ', 'SOUTH' -> 'South')**
   - Dimension: Consistency
   - Fix: strip + title case

3. **Imputing missing category using product lookup**
   - Dimension: Accuracy, Completeness
   - Fix: Every product belongs to exactly one category, so lookup is exact and deterministic. No rows dropped.

4. **Imputing missing profit_inr**
   - Dimension: Completeness, Accuracy
   - Fix: For each of 6 categories, mean(profit_inr / sales_inr) calculated, then missing profit_inr = sales_inr * category_mean_margin. Rounded to 2 decimals.

5. **Generating order_date (was missing in raw)**
   - Dimension: Completeness, Timeliness
   - Fix: Generated from 2023-01-01 range

6. **Removing rows with negative sales / quantity (if any)**
   - Dimension: Validity

## Task 1.3 - Schema Validation
- Function: validate_schema(df, required_columns)
- Required Columns: [order_id, order_date, region, category, product, quantity, sales_inr, profit_inr]
- VALID case: status = validated, missing = []
- BLOCKED case: profit_inr column dropped, status = blocked_schema, missing = [profit_inr]
- Logs: logs/clean.log and logs/schema_validation.log

## Task 1.2 / 1.3 Output
- Clean data saved as: data/pharmeasy_orders_clean.csv
- Task 1 Status: DONE, Part 2 will consume this exact cleaned data.