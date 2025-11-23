from abc import ABC, abstractmethod
from typing import List


class LLMInterface(ABC):
    """
    Abstract interface for LLM implementations.
    CRITICAL: All implementations must follow this interface.
    Reference: REWRITE_SPECIFICATION.md lines 695-720
    """

    @abstractmethod
    def generate(
        self,
        messages: List[dict],
        response_format: dict = None,
        temperature: float = 0.0
    ) -> dict:
        """
        Generate completion from LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'
            response_format: Pydantic model for structured output
            temperature: Sampling temperature (0.0 = deterministic)

        Returns:
            dict: Parsed response matching response_format
        """
        pass
