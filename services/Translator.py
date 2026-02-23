from langchain_core.tools import BaseTool
from langchain_ollama import OllamaLLM
from response import TranslationResponse
from config import LLMConfig
class Translator(BaseTool):
    name: str = "Translator"
    description: str = "A tool for translating text between languages using a specified model."
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._llm = self._init_llm()
    
    def _init_llm(self) -> OllamaLLM:
        _llm_config = LLMConfig()
        return OllamaLLM(
            model=_llm_config.model_name,
            temperature=_llm_config.temperature,
            verbose=_llm_config.verbose,
            base_url=_llm_config.base_url
        )
    
    def _run(self) -> TranslationResponse:
        pass
