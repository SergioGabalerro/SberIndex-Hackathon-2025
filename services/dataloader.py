from pathlib import Path
import pandas as pd

class DataLoader:
    """Lazy parquet/xlsx loader with simple helpers"""
    def __init__(self, data_dir: str | Path | None = None):
        self.base = Path(data_dir or Path(__file__).parents[2] / 'data')
        self._cache: dict[str, pd.DataFrame] = {}

    def _load(self, filename: str) -> pd.DataFrame:
        if filename not in self._cache:
            path = self.base / filename
            if not path.exists():
                raise FileNotFoundError(path)
            if filename.endswith('.parquet'):
                self._cache[filename] = pd.read_parquet(path)
            elif filename.endswith('.xlsx'):
                self._cache[filename] = pd.read_excel(path)
            else:
                raise ValueError('Unsupported file type')
        return self._cache[filename]

    # Convenience wrappers
    def population(self, year: int) -> pd.DataFrame:
        df = self._load('2_bdmo_population.parquet')
        return df[df['year'] == year]

    def salary(self, year: int, okved_letter: str) -> pd.DataFrame:
        df = self._load('4_bdmo_salary.parquet')
        return df[(df['year'] == year) & (df['okved_letter'] == okved_letter)]

    def market_access(self, year: int) -> pd.DataFrame:
        df = self._load('1_market_access.parquet')
        return df[df['year'] == year]

    def table_exists(self, filename: str) -> bool:
        return (self.base / filename).exists()

    def column_exists(self, filename: str, column: str) -> bool:
        if not self.table_exists(filename):
            return False
        df = self._load(filename)
        return column in df.columns
