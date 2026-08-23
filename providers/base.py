from abc import ABC, abstractmethod

class LLMProvider(ABC):

    # Defines the method that every provider must implement.
    @abstractmethod
    def generate(self, messages, tools):
        pass