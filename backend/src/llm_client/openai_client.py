from .base import LLMClientMessages Prompt LLMClientBase

class LLMClient(LLMClientBase):

    def get_llm_api(message: LLMClientMessages) -> dictionary:
        return openai_client.chat.completions.create(model = LLMClientMessage["model"], messages = LLMClientMessages.["messages"])
