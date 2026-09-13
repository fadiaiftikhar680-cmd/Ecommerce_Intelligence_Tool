"""Google Gemini integration for merchant intelligence responses."""

import os
from typing import Any, Dict, Optional

import requests


class GeminiServiceError(RuntimeError):
    """Raised when Gemini configuration or generation fails."""


class GeminiService:
    """Small REST client that keeps Gemini credentials outside application code."""

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.timeout = float(os.getenv("GEMINI_TIMEOUT_SEC", "30"))

    def generate_insight(
        self,
        question: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Generate a concise Pakistan e-commerce insight with Gemini."""
        if not self.api_key:
            raise GeminiServiceError("GEMINI_API_KEY is not configured on the backend.")

        context_text = "No additional merchant context was provided."
        if context:
            context_text = "Merchant context:\n" + "\n".join(
                f"- {key}: {value}" for key, value in context.items()
            )

        prompt = (
            "You are a practical Pakistan e-commerce intelligence assistant. "
            "Give concise, actionable advice in the user's language. "
            "Do not invent live prices, laws, courier policies, or statistics. "
            "Clearly label assumptions when information is missing.\n\n"
            f"{context_text}\n\n"
            f"Merchant question:\n{question.strip()}"
        )
        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )

        try:
            response = requests.post(
                endpoint,
                params={"key": self.api_key},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            raise GeminiServiceError("Gemini API request failed.") from exc
        except ValueError as exc:
            raise GeminiServiceError("Gemini returned invalid JSON.") from exc

        try:
            text = payload["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise GeminiServiceError("Gemini returned no usable answer.") from exc

        if not isinstance(text, str) or not text.strip():
            raise GeminiServiceError("Gemini returned an empty answer.")
        return text.strip()


gemini_service = GeminiService()
