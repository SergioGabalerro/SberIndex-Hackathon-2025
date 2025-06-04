import re, yaml, json
from pathlib import Path
from utils.logger import get_logger

_log = get_logger('Classifier')

class QueryClassifier:
    def __init__(self):
        cfg_path = Path(__file__).parents[1] / 'config' / 'tasks.yml'
        with open(cfg_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def classify(self, question: str) -> dict:
        q_lower = question.lower()
        task = None
        for t, props in self.config.items():
            if any(s in q_lower for s in props['synonyms']):
                task = t
                break
        if task is None:
            raise ValueError('Не смог определить метрику в вопросе')
        year_match = re.search(r'(19|20)\d{2}', q_lower)
        year = int(year_match.group()) if year_match else None
        top_n = None
        if 'top' in q_lower or 'топ' in q_lower or 'самые' in q_lower:
            n_match = re.search(r'(?:top|топ|-?)(\d+)', q_lower)
            if n_match:
                top_n = int(n_match.group(1))
        okved = None
        if 'финанс' in q_lower or 'k' in q_lower.split():
            okved = 'K'
        intent = {
            'task': task,
            'year': year,
            'top_n': top_n,
            'okved': okved
        }
        _log.info(f'intent: {intent}')
        return intent
