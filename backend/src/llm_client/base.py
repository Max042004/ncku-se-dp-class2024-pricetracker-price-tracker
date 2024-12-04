import abc
from .exceptions import DomainMismatchException
from pydantic import BaseModel, Field
from typing import Dict

class LLMClientMessages(BaseModel):
    model: str = Field(
        default=...,
        example="gpt-3.5-turbo",
        description="The LLM model",
    )
    messages: list = Field(
        default=...,
        example=[{"role": "system"},{"role": "user"}],
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
        example="You are a teacher to teach college student.",
        description="The Prompt for LLM",
    )

class LLMClientBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_llm_api(prompt: Prompt) -> Dict[str, str]:
        return NotImplemented

    def validate_domain(self, domain: str):
        """
        This is an example of a method that could use DomainMismatchException.
        It raises the exception if the provided domain does not match the
        expected domain or configuration.
        """
        expected_domain = "example.com"
        if domain != expected_domain:
            raise DomainMismatchException(f"Expected domain '{expected_domain}', but got '{domain}'")
        return True
