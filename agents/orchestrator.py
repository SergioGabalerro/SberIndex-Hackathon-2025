from agents.classifier import QueryClassifier
from agents.context import ContextBuilder
from agents.answer import AnswerGenerator
from services.llm_factory import get_llm
from utils.logger import get_logger

class OrchestratorAgent:
    def __init__(self, llm_provider: str | None = None):
        self.logger = get_logger('Orchestrator')
        self.classifier = QueryClassifier()
        self.context_builder = ContextBuilder()
        self.answer_gen = AnswerGenerator()
        self.llm_provider = llm_provider or 'openai'
        self.llm = get_llm(self.llm_provider)

    def set_llm_provider(self, provider: str):
        self.llm_provider = provider
        self.llm = get_llm(provider)
        self.logger.info(f'Switched LLM to {provider}')

    def handle(self, question: str) -> str:
        try:
            intent = self.classifier.classify(question)
            df, ctx = self.context_builder.build(intent)
            return self.answer_gen.generate(df, ctx)
        except Exception as e:
            self.logger.error(e)
            return f'Ошибка: {e}'
