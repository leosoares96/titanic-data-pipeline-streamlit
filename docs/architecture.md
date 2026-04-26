# Data Architecture

## Overview

This project simulates a modern data pipeline using a fully local stack.

## Layers

### 1. Data Source

Public Titanic dataset (CSV)

### 2. Ingestion Layer

Python script responsible for extracting data

### 3. Raw Layer

Stores immutable raw data (`data/raw`)

### 4. Processing Layer

Data cleaning and feature engineering with Pandas

### 5. Storage Layer

SQLite database used as analytical storage

### 6. Serving Layer

Streamlit dashboard for data consumption

## Data Flow

`Data Source → Extract → Raw → Transform → SQLite → Streamlit`

## Design Decisions

- SQLite for simplicity and local analytics
- Separation of layers for modularity
- Batch processing for reproducibility

## Trade-offs

- Not scalable (local execution)
- No orchestration tool
- No incremental loads

## Future Improvements

- Replace SQLite with cloud data warehouse
- Add orchestration (Airflow)
- Implement data quality checks
