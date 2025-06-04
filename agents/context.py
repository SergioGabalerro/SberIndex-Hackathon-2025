from services.dataloader import DataLoader
from utils.logger import get_logger
import pandas as pd

_log = get_logger('Context')

class ContextBuilder:
    def __init__(self):
        self.dl = DataLoader()

    def build(self, intent: dict) -> tuple[pd.DataFrame, dict]:
        task = intent['task']
        year = intent.get('year')
        if task == 'population':
            df = self.dl.population(year)
        elif task == 'salary':
            df = self.dl.salary(year, intent.get('okved', 'K'))
        elif task == 'market_access':
            df = self.dl.market_access(year)
        else:
            raise ValueError(f'Неизвестная задача {task}')
        if df.empty:
            raise ValueError('Нет данных под такой запрос')
        return df, intent
