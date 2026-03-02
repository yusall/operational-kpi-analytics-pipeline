import pandas as pd


def validate_data(df: pd.DataFrame) -> dict:
    report = {}

    report["row_count"] = int(df.shape[0])
    report["column_count"] = int(df.shape[1])
    report["duplicate_rows"] = int(df.duplicated().sum())

    # Missing values summary (top 15)
    missing = df.isnull().sum().sort_values(ascending=False)
    report["missing_values_top_15"] = missing.head(15).to_dict()

    # Invalid dates checks (only for columns that exist)
    date_cols = ["booking_from", "booking_to", "expected_completion_date",
                 "job_done", "invoice_created", "invoice_paid"]
    invalid_dates = {}
    for col in date_cols:
        if col in df.columns:
            invalid_dates[col] = int(df[col].isna().sum())
    report["invalid_dates"] = invalid_dates

    # Money sanity checks
    if "invoice_amount" in df.columns:
        report["invoice_amount_missing"] = int(df["invoice_amount"].isna().sum())
        report["negative_invoices"] = int((df["invoice_amount"] < 0).sum())

    # Boolean sanity checks
    if "is_emergency" in df.columns:
        report["is_emergency_missing"] = int(df["is_emergency"].isna().sum())

    if "is_complete" in df.columns:
        report["is_complete_true_count"] = int(df["is_complete"].sum())
        report["is_complete_false_count"] = int((~df["is_complete"]).sum())

    return report