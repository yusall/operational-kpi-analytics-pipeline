import sqlite3
import pandas as pd
import os


def run_queries(db_path="company.db", output_folder="outputs/reports"):
    os.makedirs(output_folder, exist_ok=True)

    conn = sqlite3.connect(db_path)

    queries = {
        "revenue_by_client": """
            SELECT c.client_name,
                   SUM(f.invoice_amount) AS total_revenue
            FROM financials f
            JOIN jobs j ON j.enquiry_id = f.enquiry_id
            JOIN clients c ON c.client_id = j.client_id
            GROUP BY c.client_name
            ORDER BY total_revenue DESC;
        """,

        "jobs_by_category": """
            SELECT category,
                   COUNT(*) AS total_jobs
            FROM jobs
            GROUP BY category
            ORDER BY total_jobs DESC;
        """,

        "quote_acceptance_rate": """
            SELECT
              SUM(CASE WHEN LOWER(status) = 'quote_accepted' THEN 1 ELSE 0 END) * 1.0
              / COUNT(*) AS quote_acceptance_rate
            FROM jobs;
        """,

        "overdue_jobs": """
            SELECT *
            FROM jobs
            WHERE expected_completion_date IS NOT NULL
              AND expected_completion_date < DATE('now')
              AND is_complete = 0;
        """,

        "missing_invoices_on_completed": """
            SELECT j.*
            FROM jobs j
            LEFT JOIN financials f
              ON j.enquiry_id = f.enquiry_id
            WHERE j.is_complete = 1
              AND f.invoice_amount IS NULL;
        """
    }

    for name, query in queries.items():
        df = pd.read_sql_query(query, conn)
        df.to_csv(f"{output_folder}/{name}.csv", index=False)

    conn.close()