import pandas as pd


def timestamp_with_timezone(df: pd.DataFrame) -> pd.DataFrame:
    timezone_info = getattr(df["timestamp"].dt, "tz", None)
    df["source_timezone"] = str(timezone_info)
    if timezone_info is not None:
        df["timestamp"] = df["timestamp"].dt.tz_localize(None)
    df = reorder_columns(df)
    return df

def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    mandatory = ["timestamp", "source_timezone"]
    for col in mandatory:
        if col not in df.columns:
            raise KeyError(f"Missing required column: {col}")
    others = [col for col in df.columns if col not in mandatory]
    new_order = ["timestamp", "source_timezone"] + others
    return df[new_order]

def unify_timestamp_column(df: pd.DataFrame) -> pd.DataFrame:
    possible_names = ["date", "Date", "timestamp", "time", "datetime", "Datetime"]
    for name in possible_names:
        if name in df.columns:
            df = df.rename(columns={name: "timestamp"})
            return df
    raise KeyError("No column with a valid timestamp label in DataFrame.")

