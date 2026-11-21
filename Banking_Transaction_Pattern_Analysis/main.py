"""
Project 10: Banking Transaction Pattern Analysis
Industry: Banking / FinTech

IMPORTANT:
This project uses a synthetic teaching dataset. The Flagged column is a supplied
label for analysis only; it is NOT proof of fraud and must not be used to make
fraud claims or decisions about real customers.
"""

import numpy as np
import pandas as pd

import numpy as np
import pandas as pd

DATA_FILE = "10_bank_transactions.csv"


def load_data():
    """Task 139: Load and inspect transaction records."""
    data = pd.read_csv(DATA_FILE, parse_dates=["Transaction_Date"])
    print("\n========== DATASET INSPECTION ==========")
    print("First five records:\n", data.head())
    print("\nShape (rows, columns):", data.shape)
    print("\nColumn data types:\n", data.dtypes)
    print("\nDataset information:")
    data.info()
    print("\nDescriptive statistics:\n", data.describe(include="all"))
    return data


def clean_data(data):
    """Tasks 140-141: Handle missing amounts and check duplicate IDs."""
    print("\n========== DATA QUALITY ==========")
    missing_count = data["Transaction_Amount"].isna().sum()
    print("Missing transaction amounts:", missing_count)

    # Use median imputation to avoid deleting otherwise useful records.
    median_amount = data["Transaction_Amount"].median()
    data["Transaction_Amount"] = data["Transaction_Amount"].fillna(median_amount)
    print(f"Filled missing amounts with median: Rs. {median_amount:,.2f}")

    duplicate_count = data["Transaction_ID"].duplicated().sum()
    print("Duplicate Transaction_ID rows:", duplicate_count)
    if duplicate_count > 0:
        print("Duplicate IDs:\n", data.loc[data["Transaction_ID"].duplicated(keep=False),
                                            ["Transaction_ID", "Customer_ID"]].head(20))
        # Preserve rows for analysis; mark them instead of silently deleting.
        data["Duplicate_ID"] = data["Transaction_ID"].duplicated(keep=False)
    else:
        data["Duplicate_ID"] = False
    return data


def basic_financial_summary(data):
    """Tasks 142-143: Credit/debit totals and amount statistics."""
    print("\n========== CREDIT / DEBIT SUMMARY ==========")
    for transaction_type in ["Credit", "Debit"]:
        subset = data[data["Transaction_Type"] == transaction_type]
        total = subset["Transaction_Amount"].sum()
        print(f"Total {transaction_type}s: Rs. {total:,.2f} "
              f"(records: {len(subset)})")

    amounts = data["Transaction_Amount"]
    print("\n========== AMOUNT STATISTICS ==========")
    print(f"Mean: Rs. {amounts.mean():,.2f}")
    print(f"Median: Rs. {amounts.median():,.2f}")
    print(f"Standard deviation: Rs. {amounts.std():,.2f}")


def channel_and_city_analysis(data):
    """Tasks 144-145: Transaction volume by channel and value by city."""
    print("\n========== CHANNEL SUMMARY ==========")
    channel_summary = data.groupby("Channel").agg(
        Transaction_Count=("Transaction_ID", "count"),
        Total_Value=("Transaction_Amount", "sum"),
        Average_Value=("Transaction_Amount", "mean")
    ).sort_values("Transaction_Count", ascending=False)
    print(channel_summary.round(2))
    channel_summary.to_csv("channel_summary.csv")

    print("\n========== CITY SUMMARY ==========")
    city_summary = data.groupby("City").agg(
        Transaction_Count=("Transaction_ID", "count"),
        Total_Transaction_Value=("Transaction_Amount", "sum")
    ).sort_values("Total_Transaction_Value", ascending=False)
    print(city_summary.round(2))
    city_summary.to_csv("city_summary.csv")


def flagged_analysis(data):
    """Tasks 146-147: Count and percentage of supplied flagged labels."""
    print("\n========== FLAGGED RECORD SUMMARY ==========")
    flagged_count = (data["Flagged"] == "Yes").sum()
    total_count = len(data)
    flagged_percentage = (flagged_count / total_count) * 100 if total_count else 0
    print(f"Flagged-labelled records: {flagged_count} / {total_count}")
    print(f"Flagged-labelled percentage: {flagged_percentage:.2f}%")

    # Calculate within each channel; normalize=True gives proportions.
    flagged_work = data.assign(Flagged_Is_Yes=(data["Flagged"] == "Yes"))
    flagged_by_channel = flagged_work.groupby("Channel").agg(
        Total_Transactions=("Transaction_ID", "count"),
        Flagged_Count=("Flagged_Is_Yes", "sum"),
        Flagged_Percentage=("Flagged_Is_Yes", "mean")
    )
    flagged_by_channel["Flagged_Percentage"] = flagged_by_channel["Flagged_Percentage"] * 100
    print("\nFlagged percentage by channel:\n", flagged_by_channel.round(2))
    flagged_by_channel.to_csv("flagged_by_channel.csv")


def largest_transactions(data):
    """Task 148: Display the 10 largest transactions."""
    print("\n========== TOP 10 LARGEST TRANSACTIONS ==========")
    top_10 = data.nlargest(10, "Transaction_Amount")
    print(top_10[["Transaction_ID", "Transaction_Amount", "Transaction_Type",
                  "Channel", "City", "Flagged"]].to_string(index=False))
    top_10.to_csv("top_10_transactions.csv", index=False)


def account_type_comparison(data):
    """Task 149: Credit/debit totals grouped by account type."""
    print("\n========== ACCOUNT TYPE: CREDIT / DEBIT ==========")
    account_summary = data.pivot_table(
        index="Account_Type",
        columns="Transaction_Type",
        values="Transaction_Amount",
        aggfunc="sum",
        fill_value=0
    )
    print(account_summary.round(2))
    account_summary.to_csv("account_type_credit_debit.csv")

    # Also demonstrate the grouping structure suggested in the assignment.
    grouped = data.groupby(["Account_Type", "Transaction_Type"])["Transaction_Amount"].sum()
    print("\nUsing groupby(['Account_Type', 'Transaction_Type']):\n", grouped.round(2))


def outlier_analysis(data):
    """Task 150: Identify amount outliers using IQR and np.percentile()."""
    amounts = data["Transaction_Amount"].to_numpy()
    q1 = np.percentile(amounts, 25)
    q3 = np.percentile(amounts, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = data[(data["Transaction_Amount"] < lower_bound) |
                    (data["Transaction_Amount"] > upper_bound)]
    print("\n========== IQR OUTLIER ANALYSIS ==========")
    print(f"Q1: Rs. {q1:,.2f} | Q3: Rs. {q3:,.2f} | IQR: Rs. {iqr:,.2f}")
    print(f"Lower bound: Rs. {lower_bound:,.2f}")
    print(f"Upper bound: Rs. {upper_bound:,.2f}")
    print("Potential statistical outliers:", len(outliers))
    outliers.to_csv("amount_outliers_iqr.csv", index=False)


def amount_bands(data):
    """Task 151: Create transaction amount bands."""
    bins = [0, 1000, 5000, 10000, 25000, 50000, np.inf]
    labels = ["0-1,000", "1,001-5,000", "5,001-10,000",
              "10,001-25,000", "25,001-50,000", "Above 50,000"]
    data["Amount_Band"] = pd.cut(data["Transaction_Amount"], bins=bins,
                                 labels=labels, include_lowest=True)
    band_summary = data["Amount_Band"].value_counts(sort=False).rename("Count")
    print("\n========== TRANSACTION AMOUNT BANDS ==========\n", band_summary)
    band_summary.to_csv("amount_band_summary.csv")


def numpy_boolean_filter(data):
    """Task 152: NumPy Boolean indexing for transactions above a threshold."""
    print("\n========== NUMPY BOOLEAN INDEXING ==========")
    threshold = 10000  # Change this value to experiment.
    amount_array = data["Transaction_Amount"].to_numpy()
    condition = amount_array > threshold
    high_value_transactions = data.loc[condition]
    print(f"Threshold: Rs. {threshold:,.2f}")
    print("Number above threshold:", np.count_nonzero(condition))
    print(high_value_transactions[["Transaction_ID", "Transaction_Amount",
                                   "Transaction_Type", "Channel", "City"]].head(20))
    high_value_transactions.to_csv("above_threshold_transactions.csv",
                                   index=False)


def operational_observations(data):
    """Task 153: Five cautious observations and recommendations."""
    print("\n========== FIVE CAUTIOUS OPERATIONAL OBSERVATIONS ==========")
    channel_counts = data["Channel"].value_counts()
    city_values = data.groupby("City")["Transaction_Amount"].sum()
    flagged_pct = (data["Flagged"] == "Yes").mean() * 100
    duplicate_rows = data["Duplicate_ID"].sum()
    missing_filled = data["Transaction_Amount"].notna().sum()

    observations = [
        f"1. Channel usage varies: the most-used channel in this sample is "
        f"{channel_counts.idxmax()} ({channel_counts.max()} records). "
        "Recommendation: review channel capacity and customer support using verified operational data.",
        f"2. Total transaction value differs by city; {city_values.idxmax()} has the "
        "highest total in this synthetic sample. Recommendation: compare with branch size and customer base before allocating resources.",
        f"3. {flagged_pct:.2f}% of rows carry the supplied Flagged='Yes' label. "
        "Recommendation: treat this only as a dataset label and route real cases through approved review procedures.",
        f"4. {int(duplicate_rows)} rows are associated with repeated Transaction_ID values. "
        "Recommendation: validate transaction identifiers at ingestion and investigate duplicates before reporting.",
        f"5. Amount completeness after the cleaning step is {data['Transaction_Amount'].notna().mean()*100:.2f}%. "
        "Recommendation: monitor missing values and document the chosen imputation method."
    ]
    for item in observations:
        print(item)

    with open("operational_observations.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(observations))


def main():
    print("=" * 65)
    print("       BANKING TRANSACTION PATTERN ANALYSIS")
    print("=" * 65)
    data = load_data()
    data = clean_data(data)

    # Menu uses if/elif/else and a while loop, as requested.
    while True:
        print("\nChoose an analysis:")
        print("1. Run all analyses")
        print("2. Credit/debit and descriptive statistics")
        print("3. Channel and city summaries")
        print("4. Flagged-record analysis")
        print("5. Top 10 and IQR outliers")
        print("6. Account-type comparison and amount bands")
        print("7. NumPy threshold filter")
        print("8. Exit")
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            basic_financial_summary(data)
            channel_and_city_analysis(data)
            flagged_analysis(data)
            largest_transactions(data)
            account_type_comparison(data)
            outlier_analysis(data)
            amount_bands(data)
            numpy_boolean_filter(data)
            operational_observations(data)
            print("\nAll report files saved in the project folder.")
        elif choice == "2":
            basic_financial_summary(data)
        elif choice == "3":
            channel_and_city_analysis(data)
        elif choice == "4":
            flagged_analysis(data)
        elif choice == "5":
            largest_transactions(data)
            outlier_analysis(data)
        elif choice == "6":
            account_type_comparison(data)
            amount_bands(data)
        elif choice == "7":
            numpy_boolean_filter(data)
        elif choice == "8":
            print("Thank you for using the analysis project!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
