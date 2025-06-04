from pathlib import Path
import pandas as pd

class DataLoader:
    """Lazy parquet/xlsx loader with simple helpers"""
    def __init__(self, data_dir: str | Path | None = None):
        """Initialize loader.

        ``data_dir`` can be supplied explicitly for tests. If omitted, the
        loader expects a ``data`` directory in the project root. The previous
        implementation used ``parents[2]`` which pointed one level above the
        repository when running from ``services/``, resulting in an invalid
        path on both Linux and Windows.  Using ``parents[1]`` reliably locates
        the repository root.
        """
        root = Path(__file__).resolve().parents[1]
        self.base = Path(data_dir).resolve() if data_dir else root / 'data'
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
    def population(self, year: int | None) -> pd.DataFrame:
        df = self._load('2_bdmo_population.parquet')
        if year is not None:
            df = df[df['year'] == year]
        return df

    def salary(self, year: int | None, okved_letter: str) -> pd.DataFrame:
        df = self._load('4_bdmo_salary.parquet')
        if year is not None:
            df = df[df['year'] == year]
        if okved_letter is not None:
            df = df[df['okved_letter'] == okved_letter]
        return df

    def market_access(self, year: int | None) -> pd.DataFrame:
        df = self._load('1_market_access.parquet')
        if year is not None:
            df = df[df['year'] == year]
        return df

    def table_exists(self, filename: str) -> bool:
        return (self.base / filename).exists()

    def column_exists(self, filename: str, column: str) -> bool:
        if not self.table_exists(filename):
            return False
        df = self._load(filename)
        return column in df.columns