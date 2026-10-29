"""
Ollama Client Module
Course: 24CS2506 – Building Applications using GPT-4
Experiment 2: AI-Powered Blog Content Generator using Ollama
"""

import json
import requests
from typing import Dict, Any, Optional, List, Generator


class OllamaClient:
    """
    Client for interacting with local Ollama API (http://localhost:11434).
    Supports generation, model querying, and streaming responses for Llama 3.2.
    """
    def __init__(self, base_url: str = "http://localhost:11434", default_model: str = "llama3.2"):
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model
        self.is_connected = self.check_connection()

    def check_connection(self) -> bool:
        """Check if local Ollama daemon is reachable."""
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=1.5)
            return resp.status_code == 200
        except Exception:
            return False

    def list_models(self) -> List[str]:
        """List available local models in Ollama."""
        if not self.check_connection():
            return []
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=2.0)
            if resp.status_code == 200:
                data = resp.json()
                models = [m.get("name", "") for m in data.get("models", [])]
                return [m for m in models if m]
            return []
        except Exception:
            return []

    def get_best_available_model(self) -> str:
        """Return llama3.2 if available, or first available model, or default."""
        models = self.list_models()
        if not models:
            return self.default_model
        for m in models:
            if "llama3.2" in m.lower():
                return m
        for m in models:
            if "llama" in m.lower() or "qwen" in m.lower() or "mistral" in m.lower():
                return m
        return models[0]

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Optional[str]:
        """Generate response using Ollama /api/generate endpoint."""
        if not self.check_connection():
            return None

        target_model = model or self.default_model
        payload: Dict[str, Any] = {
            "model": target_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        if system:
            payload["system"] = system
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120.0
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("response", "").strip()
        except Exception:
            return None
        return None

    def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7
    ) -> Generator[str, None, None]:
        """Stream chunks from Ollama API."""
        if not self.check_connection():
            return

        target_model = model or self.default_model
        payload: Dict[str, Any] = {
            "model": target_model,
            "prompt": prompt,
            "stream": True,
            "options": {"temperature": temperature}
        }
        if system:
            payload["system"] = system

        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=120.0
            )
            for line in resp.iter_lines():
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    text = chunk.get("response", "")
                    if text:
                        yield text
                    if chunk.get("done", False):
                        break
        except Exception:
            return
