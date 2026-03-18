from __future__ import annotations

import math
import os
from typing import AsyncGenerator

from anthropic import AsyncAnthropicVertex
from dotenv import load_dotenv

from app.utils.format_message import format_user_message

load_dotenv()


class AnthropicService:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-east5")

    def _create_client(self) -> AsyncAnthropicVertex:
        return AsyncAnthropicVertex(
            project_id=self.project_id,
            region=self.location,
        )

    @staticmethod
    def estimate_tokens(text: str) -> int:
        return math.ceil(len(text) / 4)

    async def stream_completion(
        self,
        *,
        model: str,
        system_prompt: str,
        data: dict[str, str | None],
        api_key: str | None = None,
        max_output_tokens: int | None = None,
    ) -> AsyncGenerator[str, None]:
        user_prompt = format_user_message(data)
        client = self._create_client()
        try:
            async with client.messages.stream(
                model=model,
                max_tokens=max_output_tokens or 16384,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        finally:
            await client.close()

    async def count_input_tokens(
        self,
        *,
        model: str,
        system_prompt: str,
        data: dict[str, str | None],
        api_key: str | None = None,
    ) -> int:
        user_prompt = format_user_message(data)
        client = self._create_client()
        try:
            response = await client.messages.count_tokens(
                model=model,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            return response.input_tokens
        except Exception:
            return self.estimate_tokens(f"{system_prompt}\n{user_prompt}")
        finally:
            await client.close()
