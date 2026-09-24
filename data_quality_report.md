# PharmEasy Pulse - Data Quality Report

## Overview
- Clean rows: 2100
- Raw 2159 -> Clean 2100, Dupes 59

## 7 Dimensions

1. Completeness: 94 missing profit_inr, 48 missing category - Fixed by imputation
2. Consistency: Region 16 variants -> 9 canonical via keyword mapping
3. Uniqueness: 59 duplicate order_id removed with drop_duplicates
4. Validity: sales_inr, profit_inr numeric, quantity 1-10 checked
5. Accuracy: profit = sales*0.2, order_value = sales recalculated
6. Timeliness: Current 2026 data, no order_date in raw
7. Integrity: regions_master 10 (9 active + Kurnool 0 orders) referential check

## Fixes
- profit_inr: product avg 20% logic
- category: product->category map
- region: hyd->Hyderabad, mum->Mumbai etc
- dedup: keep last

## Proof
Before: 94 profit, 48 category missing
After: 0 missing
