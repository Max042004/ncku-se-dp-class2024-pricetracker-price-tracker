import abc

from .exceptions import DomainMismatchException

from pydantic import BaseModel, Field

class LLMClientMessages(BaseModel):
    model: str = Field(
        default=...,
        example="gpt-3.5-turbo",
        description="The LLM model",
    )
    messages: list = Field(
        default=...,
        example="JSON file"
        description="The Prompt for LLM",
    )

class Prompt(BaseModel):
    role: str = Field(
        default=...,
        example="system",
        description="The role of LLM",
    )
    content: str = Field(
        default=...,
        example="You are a teacher to teach college student."
        description="The Prompt for LLM",
    )

class LLMClientBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_llm_api(prompt: Prompt) -> dictionary:
        retrun NotImplemented
