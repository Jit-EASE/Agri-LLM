# ingestion/csv_processor.py
import os
import pandas as pd


def process_csv(path: str) -> dict:
    """
    Universal CSV processor for real-time analysis.
    """
    try:
        if not os.path.exists(path):
            return {"status": "error", "message": f"CSV not found: {path}"}

        df = pd.read_csv(path)

        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

        summary = df.describe(include='all').fillna("").astype(str).to_dict()

        time_cols = []
        for col in df.columns:
            try:
                pd.to_datetime(df[col])
                time_cols.append(col)
            except Exception:
                pass

        return {
            "status": "ok",
            "rows": len(df),
            "columns": df.columns.tolist(),
            "numeric_cols": numeric_cols,
            "categorical_cols": categorical_cols,
            "time_cols": time_cols,
            "summary": summary,
            "raw": df,
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
