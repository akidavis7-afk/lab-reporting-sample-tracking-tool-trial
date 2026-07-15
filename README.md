# Lab Reporting & Sample-Tracking Tool

A lightweight SQLite-backed workflow for lab managers and research assistants.

## Features

- Import sample metadata from CSV
- Required-field and duplicate checks
- Sample status tracking
- Automatic standardized folder and file names
- SQLite persistence
- Audit trail for imports and status changes
- CSV and HTML summary reports

## Local setup (Windows CMD)

```cmd
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -q
python cli.py init --db lab.db
python cli.py import --db lab.db --csv examples/samples.csv
python cli.py report --db lab.db --output outputs
streamlit run app.py
```

Open `http://localhost:8501`.

## Docker

```cmd
docker build -t lab-sample-tracker .
docker run --rm -p 8501:8501 -v "%cd%\data:/app/data" lab-sample-tracker
```

This is a prototype, not a regulated LIMS. Add authentication, backups, access controls and institutional validation before production use.

## Streamlit performance

The app uses a submit form, `st.cache_data`, immutable upload bytes, and session-state result persistence. This prevents the analysis from running again when a widget changes. The sequence-comparison apps also use a direct linear comparison for closely related equal-length sequences and reserve global alignment for likely indels or larger differences.
