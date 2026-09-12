"""
data_loader.py
---------------
Turns uploaded files (Streamlit UploadedFile objects) into pandas DataFrames,
and provides small preview helpers. No Streamlit or LangChain imports here —
keep this module UI-agnostic and easy to unit test.
"""

from dataclasses import dataclass
import pandas as pd


@dataclass
class LoadedFile:
    name: str
    dataframe: pd.DataFrame
    error: str | None = None


def load_csv_files(uploaded_files) -> list[LoadedFile]:
    """
    Convert a list of uploaded file-like objects into LoadedFile records.
    Bad/corrupt files are captured with an error message instead of raising,
    so one broken upload doesn't crash the whole app.
    """
    loaded = []
    for f in uploaded_files:
        try:
            df = pd.read_csv(f)
            loaded.append(LoadedFile(name=f.name, dataframe=df))
        except Exception as e:
            loaded.append(LoadedFile(name=f.name, dataframe=pd.DataFrame(), error=str(e)))
    return loaded


def get_preview(df: pd.DataFrame, n_rows: int = 5) -> pd.DataFrame:
    """Small head() wrapper — kept as a function in case preview logic grows later."""
    return df.head(n_rows)


def get_dataframes_dict(loaded_files: list[LoadedFile]) -> dict[str, pd.DataFrame]:
    """Returns {filename: dataframe} for only the successfully loaded files."""
    return {lf.name: lf.dataframe for lf in loaded_files if lf.error is None}