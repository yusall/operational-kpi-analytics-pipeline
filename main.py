import os
import json
from src.run_sql_analysis import run_queries
from src.data_cleaning import clean_data
from src.validation import validate_data
from src.kpi_analysis import calculate_kpis, plot_revenue_by_category, category_performance_table
from src.database_builder import build_database


def ensure_dirs():
    os.makedirs("outputs/figures", exist_ok=True)
    os.makedirs("outputs/reports", exist_ok=True)


def main():
    ensure_dirs()

    csv_path = os.getenv("CSV_PATH", "data/raw/sample_pro_jobs.csv")    
    df = clean_data(csv_path)

    # Validation
    report = validate_data(df)
    print("\nVALIDATION REPORT:")
    print(json.dumps(report, indent=2, default=str))

    with open("outputs/reports/validation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)

    # KPIs
    kpis = calculate_kpis(df)
    print("\nKPIs:")
    print(json.dumps(kpis, indent=2, default=str))

    with open("outputs/reports/kpis.json", "w", encoding="utf-8") as f:
        json.dump(kpis, f, indent=2, default=str)

    # Category table + chart
    table = plot_revenue_by_category(df, "outputs/figures/revenue_by_category.png")
    table.to_csv("outputs/reports/category_performance.csv", index=False)

    # SQLite DB
    build_database(df, db_path="company.db")
    # Run advanced SQL analytics
    run_queries()
    print("\nDONE: created outputs + company.db")


if __name__ == "__main__":
    main()