# Titanic Data Pipeline with Streamlit

## Overview

This project implements a minimal end-to-end data pipeline using the Titanic dataset.
It demonstrates core data engineering concepts such as data ingestion, transformation, quality checks, storage, and visualization — all running locally.

The goal is to simulate a modern data pipeline architecture in a simple and reproducible way.

---

## Architecture

The pipeline follows a layered approach:

- **Ingestion Layer**: Extracts raw data from a public source
- **Processing Layer**: Cleans and transforms data
- **Data Quality Layer**: Validates dataset integrity
- **Storage Layer**: Persists data in SQLite
- **Serving Layer**: Provides visualization via Streamlit

---

## Data Flow

```
Data Source (CSV)
        ↓
     Extract
        ↓
   Raw Layer (CSV)
        ↓
   Transform + Quality Checks
        ↓
Processed Data (Parquet)
        ↓
      SQLite
        ↓
    Streamlit App
```

---

## Tech Stack

- Python
- Pandas
- SQLite
- Streamlit
- PyArrow
- plotly

---

## Project Structure

```
src/
├── extract.py
├── transform.py
├── load.py
├── quality.py
└── utils/
    ├── config.py
    └── logger.py
```

---

## How to Run

### 1. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run pipeline

```
python main.py
```

### 4. Run dashboard

```
streamlit run app/app.py
```

---

## Data Quality Checks

The pipeline includes basic validation rules:

- Dataset must not be empty
- Required columns must exist
- Null percentage threshold validation

These checks help ensure data reliability before transformation.

---

## Design Decisions

- **SQLite** was chosen for simplicity and local analytical storage
- **Layered structure** improves readability and scalability
- **Batch processing** ensures reproducibility
- **Parquet format** used for efficient storage in processed layer

---

## Trade-offs

- Not designed for large-scale data processing
- No orchestration tool (e.g., Airflow)
- No incremental data loading
- Limited data quality rules

---

## Future Improvements

- Add orchestration layer (Airflow or similar)
- Migrate storage to cloud (S3 + Athena / BigQuery)
- Implement incremental loads
- Enhance data quality validation
- Improve Streamlit dashboard with filters and metrics

---

## Notes

- Data is not versioned in the repository
- The pipeline must be executed to generate local data files

---

## Purpose

This project is intended as a practical demonstration of data engineering fundamentals, focusing on clarity, structure, and reproducibility rather than complexity.
