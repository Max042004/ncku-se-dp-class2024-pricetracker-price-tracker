from .base import LLMClientMessages, LLMClientBase
from openai import OpenAI
from typing import Dict

class LLMClient(LLMClientBase):

    def get_llm_api(message: LLMClientMessages) -> Dict[str, str]:
        return openai_client.chat.completions.create(model = LLMClientMessage.model, messages = LLMClientMessages.messages)
