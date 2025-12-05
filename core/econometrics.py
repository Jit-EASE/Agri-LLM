# core/econometrics.py
import os
import pandas as pd
import statsmodels.api as sm


def econometric_module(prepared: dict, csv_result=None) -> dict:
    """
    Econometric forecast engine (same logic as your original).
    """
    if csv_result and csv_result.get("status") == "ok":
        try:
            df = csv_result["raw"]
            num_df = df.select_dtypes(include=["number"])
            if num_df.shape[1] >= 2:
                dep_col = num_df.columns[-1]
                X = sm.add_constant(num_df.iloc[:, :-1])
                y = num_df[dep_col]
                model = sm.OLS(y, X).fit()
                prediction = float(model.predict(X.iloc[-1:])[0])
                return {
                    "econometric_prediction": prediction,
                    "summary": (
                        f"Source: uploaded CSV\n"
                        f"Dependent variable: {dep_col}\n"
                        f"Regressors: {', '.join(num_df.columns[:-1])}\n\n"
                        + model.summary().as_text()
                    ),
                }
        except Exception:
            pass

    # realtime.csv path
    try:
        if os.path.exists("realtime.csv"):
            df = pd.read_csv("realtime.csv")
            num_df = df.select_dtypes(include=["number"])
            if num_df.shape[1] >= 2:
                dep_col = num_df.columns[-1]
                X = sm.add_constant(num_df.iloc[:, :-1])
                y = num_df[dep_col]

                model = sm.OLS(y, X).fit()
                prediction = float(model.predict(X.iloc[-1:])[0])

                return {
                    "econometric_prediction": prediction,
                    "summary": (
                        f"Source: realtime.csv\n"
                        f"Dependent variable: {dep_col}\n"
                        f"Regressors: {', '.join(num_df.columns[:-1])}\n\n"
                        + model.summary().as_text()
                    ),
                }
    except Exception:
        pass

    # ireland_dairy_panel.csv static model
    try:
        df = pd.read_csv("ireland_dairy_panel.csv")
        required_cols = ["price", "feed_cost", "milk_output", "profit"]
        if not all(col in df.columns for col in required_cols):
            raise ValueError("Required columns missing in ireland_dairy_panel.csv")

        X = sm.add_constant(df[["price", "feed_cost", "milk_output"]])
        y = df["profit"]
        model = sm.OLS(y, X).fit()
        prediction = float(model.predict(X.iloc[-1:])[0])

        return {
            "econometric_prediction": prediction,
            "summary": (
                "Source: ireland_dairy_panel.csv\n"
                "Dependent variable: profit\n"
                "Regressors: price, feed_cost, milk_output\n\n"
                + model.summary().as_text()
            ),
        }
    except Exception as e:
        return {
            "econometric_prediction": 0.0,
            "summary": f"Econometric model unavailable: {e}",
        }
