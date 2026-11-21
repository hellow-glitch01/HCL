# Project 10: Banking Transaction Pattern Analysis

**Industry:** Banking / FinTech  
**Language:** Python  
**Libraries:** Pandas and NumPy  
**Dataset:** `10_bank_transactions.csv` (1,500 synthetic rows)

## Important dataset note
This is a synthetic educational dataset. `Flagged` is a supplied label for practice only. It is not proof of fraud and must not be used to make fraud claims or decisions about real customers.

## Project objectives
This project completes assignment tasks 139–153:
1. Load and inspect records.
2. Find and handle missing transaction amounts (median imputation).
3. Check duplicate `Transaction_ID` values (mark them; preserve records).
4. Calculate total credits and debits.
5. Calculate mean, median and standard deviation.
6. Compare transaction volume by channel.
7. Compare total transaction value by city.
8. Calculate flagged-label count and percentage.
9. Compare flagged percentages by channel.
10. Find the 10 largest transactions.
11. Group credit/debit totals by account type.
12. Identify amount outliers using IQR with `np.percentile()`.
13. Create transaction amount bands.
14. Use NumPy Boolean indexing for amounts above a threshold.
15. Print five cautious operational observations and recommendations.

## Concepts demonstrated
- Variables, data types, operators and functions
- `if`, `elif`, `else`
- `while` loop and `for` loop
- Pandas DataFrames, filtering, `groupby`, `agg`, `pivot_table`, `nlargest`, `isna`, `fillna`
- NumPy arrays, `np.percentile`, Boolean masks and `np.count_nonzero`
- CSV input/output and basic data cleaning

## Folder structure
```text
Banking_Transaction_Pattern_Analysis/
├── 10_bank_transactions.csv
├── main.py
├── requirements.txt
├── README.md
├── SRS_Document.md
└── outputs/                 # Created automatically after analyses run
```

## Setup in VS Code
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open Terminal → New Terminal.
4. Create and activate a virtual environment (recommended).

### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

5. Install libraries:
```bash
python -m pip install -r requirements.txt
```
6. Run:
```bash
python main.py
```
7. Choose option `1` to run all analyses. Choose `8` to exit.

## Generated output files
Running option 1 creates CSV/text reports in the `outputs` folder:
- `channel_summary.csv`
- `city_summary.csv`
- `flagged_by_channel.csv`
- `top_10_transactions.csv`
- `account_type_credit_debit.csv`
- `amount_outliers_iqr.csv`
- `amount_band_summary.csv`
- `above_threshold_transactions.csv`
- `operational_observations.txt`

## Dataset columns
| Column | Description |
|---|---|
| Transaction_ID | Unique-looking transaction reference; a small number of duplicates are intentionally included for the assignment |
| Customer_ID | Synthetic customer reference |
| Transaction_Date | Synthetic transaction date |
| Transaction_Amount | Amount in INR; a few values are intentionally missing |
| Transaction_Type | Credit or Debit |
| Channel | ATM, UPI, Net Banking, Debit Card, Credit Card, Mobile Banking or Branch |
| City | Synthetic transaction city |
| Account_Type | Savings, Current, Salary or Fixed Deposit |
| Status | Completed, Pending or Failed |
| Flagged | Synthetic supplied label: Yes or No |

## Interpretation cautions
- Missing values are imputed with the median so the remaining analyses can run; document this choice in your submission.
- Duplicate transaction IDs are marked, not silently removed, so you can inspect the records.
- IQR outliers are statistical extremes, not necessarily errors or suspicious activity.
- A flagged label is not proof of fraud.
- The generated dataset is synthetic and does not describe real customers, banks or transactions.

## Suggested GitHub repository description
`A beginner-friendly Python project using Pandas and NumPy to analyze synthetic banking transaction patterns, data quality, channel and city summaries, credit/debit totals, IQR outliers and flagged labels.`
