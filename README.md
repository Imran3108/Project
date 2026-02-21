# Vulnerability Detection System (Hybrid ML + Static Analysis)

This project extends a GitHub PR Webhook backend to automatically detect security vulnerabilities in Pull Requests using a **Hybrid Approach**: 
1.  **Rule-Based Static Analysis** (Regex)
2.  **Machine Learning** (Logistic Regression / Random Forest)

## Features
*   **Automated Scanning**: Scans every new PR for vulnerabilities.
*   **SQL Injection & XSS Detection**: Uses regex patterns to find known issues.
*   **ML-Based Detection**: Trained on a dataset of vulnerable code to spot intelligent patterns.
*   **Hybrid Logic**: Combines both engines for high-accuracy results (High/Medium/Safe).
*   **Database Logging**: Stores every scan result in SQLite (`vulnerability_results.db`).
*   **Dashboard**: A Flask-based web interface to view live results.

## Project Structure
*   `webhook.py`: The main entry point. Receives GitHub events and triggers validaton.
*   `hybrid_detector.py`: The brain that orchestrates Static + ML analysis.
*   `ml_model.py`: Trains and runs the Machine Learning models.
*   `static_analysis.py`: Runs regex-based checks for hardcoded secrets, eval(), etc.
*   `database.py`: Handles data storage.
*   `dashboard.py`: Monitoring UI.
*   `dataset.csv`: Training data for the ML model.

## Setup & Installation

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Backend**:
    ```bash
    python -m uvicorn main:app --reload
    ```
    *Server listens on `http://127.0.0.1:8000/webhook`*

3.  **Run the Dashboard**:
    ```bash
    python dashboard.py
    ```
    *Dashboard available at `http://localhost:5000/dashboard`*

## Verification & Testing

*   **Train/Test ML Models**:
    ```bash
    python ml_model.py
    ```
    *(Generates `model_comparison.png` accuracy chart)*

*   **Run Integration Demo**:
    ```bash
    python demo_integration.py
    ```
    *(Simulates 5 PRs and saves results to DB)*

## Accuracy Notes
The ML model accuracy depends on the `dataset.csv`. Currently, it uses a demonstration dataset. For production use, expand the dataset with thousands of examples.
