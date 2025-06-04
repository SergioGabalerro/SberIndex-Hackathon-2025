import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
try:
    from langchain_gigachat import GigaChat
except ImportError:
    GigaChat = None

def get_llm(provider: str = None, temperature: float = 0.0):
    provider = provider or os.getenv('LLM_PROVIDER', 'openai').lower()
    if provider == 'gigachat':
        if GigaChat is None:
            raise RuntimeError('langchain-gigachat not installed')
        token = os.getenv('GIGACHAT_TOKEN')
        if not token:
            raise RuntimeError('GIGACHAT_TOKEN not set')
        return GigaChat(
            credentials={'GIGACHAT_TOKEN': token},
            model='GigaChat-Pro',
            verify_ssl_certs=False,
            temperature=temperature
        )
    # default: openai
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        raise RuntimeError('OPENAI_API_KEY not set')
    return ChatOpenAI(model_name='gpt-4o-mini', api_key=key, temperature=temperature)
