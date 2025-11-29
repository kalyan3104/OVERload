import os
from config import OPENAI_API_KEY

FORWARDER = os.getenv("FORWARDER", "mock")


def call_llm_mock(prompt: str) -> str:
    return "MOCK LLM: (the prompt was received and processed in safe mode)."


def call_openai(prompt: str):
    import openai

    openai.api_key = OPENAI_API_KEY
    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
    )
    return resp.choices[0].message["content"]


def forward_prompt(prompt: str) -> str:
    if FORWARDER == "openai" and OPENAI_API_KEY:
        return call_openai(prompt)
    else:
        return call_llm_mock(prompt)
