import os, asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from agents.orchestrator import OrchestratorAgent
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()
log = get_logger('Bot')

TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise RuntimeError('TELEGRAM_TOKEN not set in .env')

bot = Bot(
    TOKEN,
    default=DefaultBotProperties(parse_mode='HTML')              # ★ новое API
)
dp = Dispatcher()
orch = OrchestratorAgent()

@dp.message(Command('start'))
async def start(msg: types.Message):
    await msg.answer('Привет! Напиши статистический вопрос, например:\n«Самые населённые МО 2024» или «Где была максимальная зарплата в отрасли K в 2024?»')

@dp.message(Command('model'))
async def change_model(msg: types.Message):
    parts = msg.text.split(maxsplit=1)
    if len(parts) != 2:
        await msg.answer('Укажите модель: /model gigachat|openai')
        return
    model = parts[1].lower()
    orch.set_llm_provider(model)
    await msg.answer(f'Переключил модель на {model}')

@dp.message()
async def any_msg(msg: types.Message):
    answer = orch.handle(msg.text)
    MAX_LEN = 4096  # Telegram message character limit
    for i in range(0, len(answer), MAX_LEN):
        await msg.answer(answer[i:i + MAX_LEN])

if __name__ == '__main__':
    import asyncio
    async def run():
        await dp.start_polling(bot)

    asyncio.run(run())
