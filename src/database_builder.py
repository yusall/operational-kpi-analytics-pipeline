import sqlite3
import pandas as pd


def build_database(df: pd.DataFrame, db_path: str = "company.db") -> None:
    conn = sqlite3.connect(db_path)

    # ----- clients -----
    if "client_name" not in df.columns:
        raise KeyError("Missing client_name (Client name)")

    clients = (
        df[["client_name"]]
        .dropna()
        .drop_duplicates()
        .sort_values("client_name")
        .reset_index(drop=True)
    )
    clients["client_id"] = clients.index + 1  # stable surrogate key

    clients.to_sql("clients", conn, if_exists="replace", index=False)

    # Map client_id back into df
    df2 = df.merge(clients, on="client_name", how="left")

    # ----- jobs/enquiries -----
    job_cols = [
        "enquiry_id",
        "enquiry_type",
        "client_id",
        "category",
        "status",
        "is_emergency",
        "booking_from",
        "booking_to",
        "expected_completion_date",
        "job_done",
        "is_complete",
    ]
    jobs = df2[[c for c in job_cols if c in df2.columns]].drop_duplicates(subset=["enquiry_id"])
    jobs.to_sql("jobs", conn, if_exists="replace", index=False)

    # ----- financials -----
    fin_cols = [
        "enquiry_id",
        "invoice_id",
        "invoice_created",
        "invoice_paid",
        "invoice_amount",
        "invoice_vat",
        "accepted_quote_amount",
        "accepted_quote_vat",
    ]
    financials = df2[[c for c in fin_cols if c in df2.columns]].copy()
    financials.to_sql("financials", conn, if_exists="replace", index=False)

    conn.close()