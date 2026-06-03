from google import genai
from google.genai import types


class Gemini:
    def __init__(self, model: str, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def add_user_message(self, messages: list, message):
        if isinstance(message, list):
            parts = message
        else:
            parts = [types.Part(text=str(message))]

        messages.append(types.Content(role="user", parts=parts))

    def add_model_message(self, messages: list, response):
        if response.candidates and response.candidates[0].content:
            messages.append(response.candidates[0].content)

    def text_from_message(self, response) -> str:
        if response.text:
            return response.text

        if not response.candidates or not response.candidates[0].content:
            return ""

        return "\n".join(
            part.text
            for part in response.candidates[0].content.parts or []
            if part.text
        )

    def has_tool_calls(self, response) -> bool:
        if not response.candidates or not response.candidates[0].content:
            return False

        return any(
            part.function_call
            for part in response.candidates[0].content.parts or []
        )

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=None,
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ):
        config_params = {
            "temperature": temperature,
            "max_output_tokens": 8000,
        }

        if stop_sequences:
            config_params["stop_sequences"] = stop_sequences

        if system:
            config_params["system_instruction"] = system

        if tools:
            config_params["tools"] = [
                types.Tool(function_declarations=tools)
            ]

        if thinking:
            config_params["thinking_config"] = types.ThinkingConfig(
                thinking_budget=thinking_budget
            )

        return self.client.models.generate_content(
            model=self.model,
            contents=messages,
            config=types.GenerateContentConfig(**config_params),
        )
