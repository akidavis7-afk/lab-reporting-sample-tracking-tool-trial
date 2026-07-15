from __future__ import annotations

import io
import os

import pandas as pd
import streamlit as st
import yaml

from src.core import audit_log, import_csv, init_db, list_samples, update_status


@st.cache_data(show_spinner=False, max_entries=20)
def parse_sample_csv(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(file_bytes))


with open("configs/default.yaml", encoding="utf-8") as handle:
    cfg = yaml.safe_load(handle) or {}

DB = os.getenv("LAB_DB", "lab.db")
REQUIRED_COLUMNS = cfg.get("required_columns", ["sample_id", "project", "sample_type", "owner", "status"])
init_db(DB)

st.set_page_config(page_title=cfg.get("app_title", "Lab Reporting & Sample-Tracking Tool"), layout="wide")
st.title(cfg.get("app_title", "Lab Reporting & Sample-Tracking Tool"))
st.caption("Prototype sample tracking with SQLite persistence and an audit trail.")

tab_samples, tab_import, tab_audit = st.tabs(["Samples", "Import", "Audit"])

with tab_samples:
    samples = list_samples(DB)
    st.dataframe(samples, use_container_width=True, hide_index=True)

    if not samples.empty:
        with st.form("status_update_form"):
            sample_id = st.selectbox("Sample to update", samples["sample_id"].tolist())
            status = st.selectbox(
                "New status",
                ["planned", "received", "processing", "complete", "archived"],
            )
            submitted = st.form_submit_button("Update status", type="primary")

        if submitted:
            update_status(DB, sample_id, status)
            st.success(f"Updated {sample_id} to {status}.")
            st.rerun()

    st.download_button(
        "Download samples",
        samples.to_csv(index=False).encode("utf-8"),
        "samples.csv",
        "text/csv",
    )

with tab_import:
    with st.form("sample_import_form"):
        uploaded_file = st.file_uploader("Sample metadata CSV", type=["csv"])
        submitted = st.form_submit_button("Validate and import", type="primary")

    if submitted:
        if uploaded_file is None:
            st.error("Upload a sample metadata CSV.")
        else:
            try:
                frame = parse_sample_csv(uploaded_file.getvalue())
                issues = import_csv(DB, frame, REQUIRED_COLUMNS)
                if not issues.empty:
                    st.dataframe(issues, use_container_width=True, hide_index=True)
                else:
                    st.success("Imported successfully.")
                    st.rerun()
            except Exception as exc:
                st.exception(exc)

with tab_audit:
    st.dataframe(audit_log(DB), use_container_width=True, hide_index=True)
