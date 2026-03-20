"""Утилиты

В этом файле собраны различные функции-утилиты и константы,
которые помогают в рутинной работе с нейросетями и генерацией.
"""

import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Union
from pydantic import BaseModel

from langchain_gigachat import GigaChat
from langchain_google_genai import ChatGoogleGenerativeAI


def setup_env() -> None:
    # Ищем .env и в текущей директории, и уровнем выше.
    cur_dir = Path.cwd()
    env_candidates = [
        cur_dir / '.env',
        cur_dir.parent / '.env',
    ]
    for env_path in env_candidates:
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)


setup_env()
credentials_gigachat = os.getenv("AUTHORIZATION_KEY")
gigachat_scope = os.getenv("SCOPE")
ca_bundle_file = os.getenv("CA_BUNDLE_FILE")

google_api_key_list = []
for i in range(1, 10):
    api_key = os.getenv(f"GOOGLE_API_KEY_{i}", 'None')
    if api_key != 'None':
        google_api_key_list.append(api_key)
    else:
        break


gemini_model_list = [
    # Подробнее: https://ai.google.dev/gemini-api/docs/pricing?hl=ru
    'gemini-3.1-flash-lite-preview',
    'gemini-3-flash-preview',
    'gemini-2.5-pro',
    'gemini-2.5-flash',
    'gemini-2.5-flash-lite',
]

def _extract_tag(text: str, tag: str) -> Optional[str]:
    match = re.search(fr"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1).strip() if match else None


def _slugify(title: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", title.lower(), flags=re.UNICODE)
    cleaned = re.sub(r"\s+", "-", cleaned.strip())
    return cleaned


def get_llm(name: str,
            temperature: float = 0.7,
            structured: BaseModel = None,
            google_api_key = None) -> Optional[Union[GigaChat, ChatGoogleGenerativeAI]]:
    llm = None

    if name.lower() == "gigachat":
        if not credentials_gigachat:
            return None
        llm = GigaChat(
            credentials=credentials_gigachat,
            scope=gigachat_scope,
            model="GigaChat",
            temperature=temperature,
            verify_ssl_certs=False,
            ca_bundle_file=ca_bundle_file,
        )

    elif name in gemini_model_list:
        if google_api_key is None:
            return None
        kwargs = dict(
            model=name,
            temperature=temperature,
            retries=1,
            request_timeout=30,
        )
        if google_api_key:
            kwargs["api_key"] = google_api_key
        llm = ChatGoogleGenerativeAI(**kwargs)
    
    if llm is not None and structured is not None:
        llm = llm.with_structured_output(structured)

    return llm


def get_response_text(response) -> str:
    content = getattr(response, "content", response)

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        chunks = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                chunks.append(item["text"])
            else:
                chunks.append(str(item))
        return "".join(chunks).strip()

    return str(content)


def get_concepts():
    with open(Path.cwd().parent / 'ontology.json', 'r', encoding='utf-8') as file:
        ontology = json.load(file)
    concepts = [
        (id, concept)
        for id, concept in ontology['labels'].items()
        if id[0] == 'Q'
    ]
    return concepts
