from langchain_core.tools import BaseTool
from typing import Optional
from langchain_ollama import OllamaLLM
from response import TranslationResponse
from config import LLMConfig
from response import TranslationInput, TranslationResponse



class Translator(BaseTool):
    name: str = "Translator"
    description: str = "A tool for translating text between languages using a specified model."
    inputs: Optional[TranslationInput] = None
    _llm : Optional[OllamaLLM] = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self._llm = self._init_llm()
    
    def _init_llm(self) -> OllamaLLM:
        _llm_config = LLMConfig()
        return OllamaLLM(
            model=self.inputs.model,
            temperature=_llm_config.temperature,
            verbose=_llm_config.verbose,
            base_url=_llm_config.base_url
        )
    
    def _run(self) -> TranslationResponse:
        if self.inputs is None:
            raise ValueError("TranslationInput is required to run the translator.")
        prompt = self._build_translation_prompt()
        response = self._llm.invoke(
            prompt,
            format=TranslationResponse.model_json_schema()
            )
        return TranslationResponse.model_validate_json(response)

    def _build_translation_prompt(self) -> str:
        prompt =  f"""
        You are a professional {self.inputs.source_lang} ({self.inputs.source_lang_code}) to {self.inputs.target_lang} ({self.inputs.target_lang_code}) translator. Your goal is to accurately convey the meaning and nuances of the original {self.inputs.source_lang} text while adhering to {self.inputs.target_lang} grammar, vocabulary, and cultural sensitivities.
        Produce only the {self.inputs.target_lang} translation, without any additional explanations or commentary. Please translate the following {self.inputs.source_lang} text into {self.inputs.target_lang}:

        {self.inputs.text}
        """
        print(f"Constructed prompt: {prompt}")
        return prompt

    def translate(self, translation_input: TranslationInput) -> str:
        self.inputs = translation_input
        self._llm = self._init_llm()
        response = self._run()
        return response.translated_text.strip()
