"""Langflow component that talks to the Deep Flo runtime."""

from __future__ import annotations

import os

import httpx

from langflow.custom.custom_component.component import Component
from langflow.inputs.inputs import IntInput, MessageTextInput, StrInput
from langflow.schema.data import Data
from langflow.template.field.base import Output


class DeepFloRuntimeComponent(Component):
    display_name = "Deep Flo Runtime"
    description = "Call the external Deep Flo Deep Agents runtime over HTTP."
    icon = "Bot"

    inputs = [
        StrInput(
            name="runtime_url",
            display_name="Runtime URL",
            value=os.getenv("DEEP_FLO_RUNTIME_URL", "http://127.0.0.1:8011"),
            info="Base URL of the Deep Flo runtime.",
        ),
        MessageTextInput(
            name="prompt",
            display_name="Prompt",
            info="Prompt to send to the Deep Flo runtime.",
            tool_mode=True,
        ),
        StrInput(
            name="thread_id",
            display_name="Thread ID",
            value="langflow-thread",
            info="Conversation thread identifier used by Deep Flo.",
            advanced=True,
        ),
        IntInput(
            name="timeout_seconds",
            display_name="Timeout Seconds",
            value=120,
            info="HTTP timeout for the runtime call.",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Response", name="response", method="run_deep_flo"),
    ]

    def run_deep_flo(self) -> Data:
        url = self.runtime_url.rstrip("/") + "/invoke"
        payload = {"prompt": self.prompt, "thread_id": self.thread_id}
        try:
            with httpx.Client(timeout=float(self.timeout_seconds)) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
            result = response.json()
        except httpx.HTTPStatusError as exc:
            result = {
                "error": f"Deep Flo runtime returned {exc.response.status_code}",
                "detail": exc.response.text,
            }
        except httpx.HTTPError as exc:
            result = {
                "error": "Deep Flo runtime request failed",
                "detail": str(exc),
            }
        data = Data(
            text=result.get("output_text", result.get("detail", result.get("error", ""))),
            data=result,
        )
        self.status = data
        return data
