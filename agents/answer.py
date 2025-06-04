import pandas as pd
from utils.logger import get_logger

_log = get_logger('Answer')

class AnswerGenerator:
    def generate(self, df: pd.DataFrame, intent: dict) -> str:
        task = intent['task']
        year = intent.get('year')
        top_n = intent.get('top_n') or 10
        if task == 'population':
            grp = df.groupby('municipality_name', as_index=False)['value'].sum()
            top = grp.nlargest(top_n, 'value')
            lines = [f"{i+1}. {row['municipality_name']} — {row['value']:,}" 
                     for i, row in top.iterrows()]
            return "\n".join(lines)
        elif task == 'salary':
            row = df.loc[df['value'].idxmax()]
            return (f"Максимальная средняя зарплата в {year} г. в отрасли 'K' была в "
                    f"{row['municipality_name']} — {row['value']:,} ₽")
        elif task == 'market_access':
            top = df.nsmallest(top_n, 'market_access')
            lines = [f"{i+1}. {row['municipality_name']} — {row['market_access']:.2f}" 
                     for i, row in top.iterrows()]
            return "\n".join(lines)
        else:
            return 'Не знаю, как ответить'
