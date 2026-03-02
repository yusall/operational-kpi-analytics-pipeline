-- ==========================================
-- Revenue by Client
-- ==========================================
SELECT
  c.client_name,
  SUM(f.invoice_amount) AS total_revenue
FROM financials f
JOIN jobs j ON j.enquiry_id = f.enquiry_id
JOIN clients c ON c.client_id = j.client_id
GROUP BY c.client_name
ORDER BY total_revenue DESC;


-- ==========================================
-- Jobs by Category
-- ==========================================
SELECT
  category,
  COUNT(*) AS total_jobs
FROM jobs
GROUP BY category
ORDER BY total_jobs DESC;


-- ==========================================
-- Quote Acceptance Rate
-- ==========================================
SELECT
  SUM(CASE WHEN LOWER(status) = 'quote_accepted' THEN 1 ELSE 0 END) * 1.0
  / COUNT(*) AS quote_acceptance_rate
FROM jobs;


-- ==========================================
-- Overdue Jobs (not completed and past expected date)
-- ==========================================
SELECT *
FROM jobs
WHERE expected_completion_date IS NOT NULL
  AND expected_completion_date < DATE('now')
  AND is_complete = 0;


-- ==========================================
-- Missing Invoices for Completed Jobs
-- ==========================================
SELECT j.*
FROM jobs j
LEFT JOIN financials f
  ON j.enquiry_id = f.enquiry_id
WHERE j.is_complete = 1
  AND f.invoice_amount IS NULL;