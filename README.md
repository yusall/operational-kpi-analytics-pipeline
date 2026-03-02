Operational KPI Analytics Pipeline

This project demonstrates an end-to-end Python data analytics pipeline for transforming raw operational job data into structured insights using Pandas, SQLite, SQL and Matplotlib.

It simulates a real-world business scenario where maintenance job records are exported as a large CSV file and require cleaning, validation, KPI calculation, database structuring and performance analysis.

Project Overview

The raw dataset contains 39 columns of operational job data, including:

Client information

Job categories

Booking and completion timestamps

Status tracking

Invoice details

Financial amounts

The objective of this project was to:

Clean and standardise messy CSV data

Validate data quality and integrity

Calculate operational and financial KPIs

Produce visual summaries

Store structured data in a relational database

Perform SQL-based performance analysis

Data Cleaning

The cleaning workflow includes:

Converting financial fields (e.g. invoice amounts) from text with commas to numeric values

Standardising date columns using pd.to_datetime

Normalising boolean values (TRUE/FALSE to True/False)

Handling missing values and inconsistent entries

Creating derived fields such as completion status

This transforms a flat spreadsheet export into structured, analysis-ready data.

Data Validation

A validation step identifies potential quality issues, including:

Missing values across columns

Invalid or unparseable dates

Duplicate rows

Negative or missing invoice amounts

Completed jobs without associated invoices

A structured validation report is generated to summarise data integrity.

Key Performance Indicators

The following KPIs are calculated:

Completion rate

Emergency job rate

Total revenue

Average revenue per job

Revenue by client

Revenue by category

Quote acceptance rate

Overdue jobs

Missing invoices on completed jobs

These metrics provide clear operational and financial insight into business performance.

Visualisation

The project generates:

Revenue by category bar chart using Matplotlib

Consolidated category performance table including:

Total jobs

Total revenue

Average revenue per job

Database Design

The cleaned dataset is structured into a relational SQLite database with three tables:

clients

jobs

financials

This replaces flat spreadsheet reporting with a normalised schema suitable for SQL querying and structured analysis.

SQL Analysis

Custom SQL queries are executed to analyse:

Revenue by client

Jobs by category

Quote acceptance rate

Overdue jobs

Completed jobs missing invoices

Query outputs are saved for reporting and further review.

Tech Stack

Python

Pandas

Matplotlib

SQLite

SQL

Project Structure
src/
  data_cleaning.py
  validation.py
  kpi_analysis.py
  database_builder.py
  run_sql_analysis.py
  generate_sample_data.py

data/
  raw/ (excluded from repository)

outputs/ (excluded from repository)

main.py
README.md
Running the Project

Generate synthetic sample data:

python src/generate_sample_data.py

Run the full pipeline:

python main.py
Notes on Data

The original dataset used during development is proprietary and is not included in this repository.
A synthetic data generator is provided to replicate the schema and allow the pipeline to run.
