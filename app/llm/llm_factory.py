import os
import yaml

from dotenv import load_dotenv
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic

load_dotenv()


class LLMFactory:
    def __init__(self, config_path="app/llm/llm_config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def get_llm(self, provider=None):
        provider = provider or self.config["default_provider"]
        provider_config = self.config["providers"][provider]

        if provider == "openai":
            return ChatOpenAI(
                model=provider_config["model"],
                temperature=provider_config["temperature"]
            )

        elif provider == "anthropic":
            return ChatAnthropic(
                model=provider_config["model"],
                temperature=provider_config["temperature"]
            )

        elif provider == "chatgroq":
            return ChatGroq(
                model_name = provider_config["model"],   # or "llama3-70b-8192"
                groq_api_key = os.getenv("GROQ_API_KEY"),
                temperature = provider_config["temperature"]
            )
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")