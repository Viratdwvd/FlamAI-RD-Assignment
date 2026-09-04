import pandas as pd


REQUIRED_COLUMNS = {"x", "y"}


def load_data(path: str) -> pd.DataFrame:
    """Load and validate the XY dataset."""

    df = pd.read_csv(path)

    if set(df.columns) != REQUIRED_COLUMNS:
        raise ValueError(
            f"Expected columns {REQUIRED_COLUMNS}, got {set(df.columns)}"
        )

    if df.empty:
        raise ValueError("Dataset is empty.")

    if not all(pd.api.types.is_numeric_dtype(df[col]) for col in REQUIRED_COLUMNS):
        raise ValueError("Columns x and y must be numeric.")

    if df[list(REQUIRED_COLUMNS)].isnull().any().any():
        raise ValueError("Dataset contains missing values.")

    if df.duplicated().any():
        raise ValueError("Dataset contains duplicate rows.")

    return df