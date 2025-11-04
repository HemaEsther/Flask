import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame):
    """
    Cleans and standardizes a pandas DataFrame.
    Steps:
    1. Normalize column names
    2. Detect & convert datatypes
    3. Handle missing values
    4. Standardize categories
    5. Handle outliers (optional)
    6. Generate summary diagnostics
    """
    # ✅ Step 1: Normalize column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace(r'[^\w]', '', regex=True)
    )

    # ✅ Step 2: Detect and convert types
    for col in df.columns:
        # Try numeric conversion
        df[col] = pd.to_numeric(df[col], errors='ignore')
        # Try datetime conversion
        if df[col].dtype == object:
            try:
                parsed = pd.to_datetime(df[col], errors='coerce', infer_datetime_format=True)
                # If at least half of column values successfully parsed as dates → use it
                if parsed.notna().sum() > len(df[col]) * 0.5:
                    df[col] = parsed
            except Exception:
                pass

    # ✅ Step 3: Handle missing values
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            mean_value = df[col].mean()
            df[col].fillna(mean_value, inplace=True)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col].fillna(pd.Timestamp("2000-01-01"), inplace=True)
        else:
            mode_value = df[col].mode()[0] if not df[col].mode().empty else "unknown"
            df[col].fillna(mode_value, inplace=True)

    # ✅ Step 4: Standardize categorical columns
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip().str.lower()
        df[col] = df[col].replace({
            'yes': True, 'no': False,
            'y': True, 'n': False
        })

    # ✅ Step 5: Handle outliers (numeric columns only)
    for col in df.select_dtypes(include=np.number).columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        # Clip outliers
        df[col] = np.clip(df[col], lower, upper)

    # ✅ Step 6: Create summary diagnostics
    summary = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": {}
    }

    for col in df.columns:
        col_data = df[col]
        col_summary = {
            "dtype": str(col_data.dtype),
            "missing_values": int(col_data.isna().sum()),
            "unique_values": int(col_data.nunique()),
        }

        if pd.api.types.is_numeric_dtype(col_data):
            col_summary.update({
                "mean": float(col_data.mean()),
                "median": float(col_data.median()),
                "std": float(col_data.std()),
                "min": float(col_data.min()),
                "max": float(col_data.max()),
            })
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            col_summary.update({
                "min_date": str(col_data.min()),
                "max_date": str(col_data.max()),
            })
        else:
            col_summary.update({
                "sample_values": col_data.unique()[:5].tolist()
            })

        summary["columns"][col] = col_summary

    return df, summary
