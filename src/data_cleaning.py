import pandas as pd

# Rename to consistent snake_case so the rest of the code is clean
RENAME_MAP = {
    "Enquiry type": "enquiry_type",
    "Enquiry ID": "enquiry_id",
    "Client name": "client_name",
    "Description": "description",
    "Category": "category",
    "Emergency": "is_emergency",
    "Status": "status",
    "Booking from": "booking_from",
    "Booking to": "booking_to",
    "Expected completion date": "expected_completion_date",
    "Job done": "job_done",
    "Invoice ID": "invoice_id",
    "Invoice created": "invoice_created",
    "Invoice paid": "invoice_paid",
    "Invoice amount": "invoice_amount",
    "Invoice VAT": "invoice_vat",
    "Accepted quote amount": "accepted_quote_amount",
    "Accepted quote VAT": "accepted_quote_vat",
    "Quote required": "quote_required",
    "DBS Job": "dbs_job",
    "Invoice contains site visit": "invoice_contains_site_visit",
    "Quote contains site visit": "quote_contains_site_visit",
    "Variation accepted": "variation_accepted",
    "Requested Variation": "requested_variation",
}

DATE_COLS = [
    "booking_from",
    "booking_to",
    "expected_completion_date",
    "job_done",
    "invoice_created",
    "invoice_paid",
    "date_quote_accepted",
    "rejected_date",
    "completion_report_signed_off_time",
]

MONEY_COLS = [
    "invoice_amount",
    "invoice_vat",
    "accepted_quote_amount",
    "accepted_quote_vat",
]

BOOL_SOURCE_COLS = [
    "is_emergency",
    "quote_required",
    "dbs_job",
    "invoice_contains_site_visit",
    "quote_contains_site_visit",
    "variation_accepted",
    "requested_variation",
]


def _to_bool(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.strip().str.lower()
    return s.map(
        {
            "true": True,
            "false": False,
            "1": True,
            "0": False,
            "yes": True,
            "no": False,
        }
    )


def _to_money(series: pd.Series) -> pd.Series:
    # Handles values like "1,077.65" and blanks
    s = series.astype(str).str.replace(",", "", regex=False).str.strip()
    s = s.replace({"": None, "nan": None, "none": None})
    return pd.to_numeric(s, errors="coerce")


def clean_data(csv_path: str) -> pd.DataFrame:
    # Read all as string first to avoid pandas doing messy auto-casting
    df = pd.read_csv(csv_path, dtype=str)

    # Strip whitespace in headers and cells
    df.columns = [c.strip() for c in df.columns]
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # Rename
    df = df.rename(columns=RENAME_MAP)

    # Booleans
    for col in BOOL_SOURCE_COLS:
        if col in df.columns:
            df[col] = _to_bool(df[col])

    # Dates (only convert cols that exist)
    for col in DATE_COLS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Money
    for col in MONEY_COLS:
        if col in df.columns:
            df[col] = _to_money(df[col])

    # Core key
    if "enquiry_id" not in df.columns:
        raise KeyError("Expected column 'Enquiry ID' in CSV (mapped to enquiry_id).")

    # Completion flag:
    # - prefer job_done (timestamp) if present
    # - otherwise infer from status if needed
    if "job_done" in df.columns:
        df["is_complete"] = df["job_done"].notna()
    else:
        df["is_complete"] = False

    # Fallback: if job_done missing or mostly empty, infer from status for robustness
    if "status" in df.columns:
        status_complete = df["status"].astype(str).str.lower().isin(
            ["invoice_paid", "completed", "done"]
        )
        df["is_complete"] = df["is_complete"] | status_complete

    # Drop records with missing enquiry_id (critical)
    df = df.dropna(subset=["enquiry_id"])

    # Optional: keep only rows with invoice_amount if you want invoice-based KPIs
    # (comment out if you want to include booked/quote stages too)
    # df = df.dropna(subset=["invoice_amount"])

    return df