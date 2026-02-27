from pydantic import BaseModel

class TranslationResponse(BaseModel):
    translated_text: str
    reasoning: str


class TranslationInput(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    source_lang_code: str
    target_lang_code: str
    model: str