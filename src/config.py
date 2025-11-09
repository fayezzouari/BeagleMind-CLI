import os
import json
from dotenv import load_dotenv

load_dotenv()

MILVUS_URI = os.getenv("MILVUS_URI")

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = "mixtral-8x7b-32768"  # or "llama2-70b-4096"

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# Vector Store Configuration
VECTOR_STORE_PATH = "repository_content"
EMBEDDINGS_MODEL = "BAAI/bge-m3"

# Reranking Configuration
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_TOP_K = 5

# Collection Configuration (env override supported)
COLLECTION_NAME = 'beagleboard'

RAG_BACKEND_URL = 'https://mind-api.beagleboard.org/api'

class ConfigManager:
    def __init__(self, path="~/.beaglemind_config.json"):
        self.path = os.path.expanduser(path)
        self.default_config = {
    "collection_name": "default_collection",
    "default_backend": "groq",
    "default_model": "mixtral-8x7b",
    "default_temperature": 0.3,
    "default_use_tools": False,
    "available_backends": ["groq", "ollama", "openai"],
    "available_models": ["mixtral-8x7b", "llama3-8b", "gpt-4o-mini"]
    }

        self.config = self.load()

    def load(self):
        # Load config from file, or create one if missing.
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(" Config file corrupted. Loading defaults.")
        else:
            # Create file if it doesn't exist
            self.save(self.default_config)
        return self.default_config.copy()

    def save(self, data=None):
        # Save current or given config to disk.
        if data is None:
            data = self.config
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def get(self, key):
        return self.config.get(key, self.default_config.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save()
