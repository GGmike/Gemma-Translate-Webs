from dataclasses import dataclass


AVAILABLE_MODELS = [
    {"value": "translategemma:4b", "label": "translategemma:4b"},
    {"value": "translategemma:12b", "label": "translategemma:12b"},
    {"value": "translategemma:27b", "label": "translategemma:27b"},
]



@dataclass(frozen=True)
class LLMConfig:
    # model_name: str 
    temperature: float = 0.0
    verbose: bool = True
    base_url: str = "http://localhost:11434"

