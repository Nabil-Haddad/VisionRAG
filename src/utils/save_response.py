import pandas as pd
from config import SHEETS_DIR


def save_results_csv(results: list[list[dict]], filename: str = "results.csv") -> None:
    rows = [row for image_rows in results for row in image_rows]
    SHEETS_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(SHEETS_DIR / filename, index=False)
    