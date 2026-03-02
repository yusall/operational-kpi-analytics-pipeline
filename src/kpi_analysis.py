import pandas as pd
import matplotlib.pyplot as plt


def calculate_kpis(df: pd.DataFrame) -> dict:
    kpis = {}

    if "is_complete" in df.columns:
        kpis["completion_rate_pct"] = float(df["is_complete"].mean() * 100)

    if "is_emergency" in df.columns:
        # mean of boolean gives proportion True
        kpis["emergency_job_rate_pct"] = float(df["is_emergency"].mean() * 100)

    if "invoice_amount" in df.columns:
        kpis["total_revenue"] = float(df["invoice_amount"].sum(skipna=True))
        kpis["avg_revenue_per_job"] = float(df["invoice_amount"].mean(skipna=True))

    # Revenue per client (topline KPI)
    if "client_name" in df.columns and "invoice_amount" in df.columns:
        per_client = (
            df.groupby("client_name", dropna=False)["invoice_amount"]
            .sum()
            .sort_values(ascending=False)
        )
        kpis["top_5_clients_by_revenue"] = per_client.head(5).to_dict()

    return kpis


def category_performance_table(df: pd.DataFrame) -> pd.DataFrame:
    if "category" not in df.columns or "invoice_amount" not in df.columns:
        raise KeyError("Need 'Category' and 'Invoice amount' columns for category performance.")

    table = (
        df.groupby("category", dropna=False)
        .agg(
            total_jobs=("enquiry_id", "count"),
            total_revenue=("invoice_amount", "sum"),
            avg_revenue_per_job=("invoice_amount", "mean"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    return table


def plot_revenue_by_category(df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    table = category_performance_table(df)

    plt.figure()
    plt.bar(table["category"].astype(str), table["total_revenue"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Revenue")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return table