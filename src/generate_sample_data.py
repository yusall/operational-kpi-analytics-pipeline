import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_sample_csv(output_path="data/raw/sample_pro_jobs.csv", n=100, seed=42):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    random.seed(seed)

    clients = ["Client A", "Client B", "Client C", "Client D"]
    categories = ["Plumber", "Flooring Specialist", "Carpenter / Joiner", "Tiler", "Handyman"]
    statuses = ["booked", "quote_accepted", "invoice_paid", "invoice_overdue"]

    rows = []
    base = datetime(2025, 1, 1)

    for i in range(n):
        enquiry_id = 1000000 + i
        client = random.choice(clients)
        category = random.choice(categories)
        status = random.choice(statuses)

        booking_from = base + timedelta(days=random.randint(0, 300))
        booking_to = booking_from + timedelta(hours=random.choice([1, 2, 3, 4, 6]))

        is_complete = status in ["invoice_paid", "invoice_overdue"]
        job_done = (booking_to + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S") if is_complete else ""

        invoice_amount = round(random.uniform(50, 2500), 2) if is_complete else ""
        invoice_paid = (booking_to + timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d %H:%M:%S") if status == "invoice_paid" else ""

        rows.append({
            "Enquiry type": "MARKETPLACE",
            "Enquiry ID": enquiry_id,
            "Client name": client,
            "Description": f"{category} job",
            "Category": category,
            "Emergency": random.choice(["FALSE", "FALSE", "FALSE", "TRUE"]),  # mostly false
            "Status": status,
            "Booking from": booking_from.strftime("%Y-%m-%d %H:%M:%S"),
            "Booking to": booking_to.strftime("%Y-%m-%d %H:%M:%S"),
            "Expected completion date": "",
            "Job done": job_done,
            "Invoice ID": "" if not is_complete else str(900000 + i),
            "Invoice created": "" if not is_complete else (booking_to + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "Invoice paid": invoice_paid,
            "Invoice amount": "" if invoice_amount == "" else f"{invoice_amount:,.2f}",  # includes commas sometimes
            "Invoice VAT": "0.00",
            "Invoice contains site visit": "FALSE",
            "Accepted quote amount": "" if not is_complete else f"{invoice_amount:,.2f}",
            "Accepted quote VAT": "0",
            "Quote required": "TRUE",
            "DBS Job": "FALSE",
            "Quote contains site visit": "FALSE",
            "Variation accepted": "FALSE",
            "Requested Variation": "FALSE",
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Saved sample dataset to {output_path}")

if __name__ == "__main__":
    generate_sample_csv()