"""Утилиты

В этом файле собраны различные функции-утилиты и константы,
которые помогают в рутинной работе с нейросетями и генерацией.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from typing import Union
from pydantic import BaseModel

from langchain_gigachat import GigaChat
from langchain_google_genai import ChatGoogleGenerativeAI


def setup_env() -> None:
    # Для деталей см .env
    cur_dir = Path.cwd()
    env_path = cur_dir.parent / '.env'
    load_dotenv(dotenv_path=env_path)


setup_env()
credentials_gigachat = os.getenv("AUTHORIZATION_KEY")

gemini_model_list = [
    # Подробнее: https://ai.google.dev/gemini-api/docs/pricing?hl=ru
    'gemini-3.1-flash-lite-preview',
    'gemini-3-flash-preview',
    'gemini-2.5-pro',
    'gemini-2.5-flash',
    'gemini-2.5-flash-lite',
    'gemini-2.5-flash-lite-preview-09-2025',
]


def get_llm(name: str,
            temperature: float = 0.7,
            structured: BaseModel = None) -> Union[GigaChat, ChatGoogleGenerativeAI]:
    llm = None
    if name == "Gigachat":
        llm = GigaChat(
            credentials=credentials_gigachat, 
            model=name,
            temperature=temperature,
            verify_ssl_certs=False,
        )

    elif name in gemini_model_list:
        llm = ChatGoogleGenerativeAI(
            model=name,
            temperature=0.7,
        )
    
    if llm is not None and structured is not None:
        llm = llm.with_structured_output(structured)

    return llm


def get_concepts():
    with open(Path.cwd().parent / 'ontology.json', 'r', encoding='utf-8') as file:
        ontology = json.load(file)

    concepts = [
        (id, concept.lower())
        for id, concept in ontology['labels'].items()
        if id[0] == 'Q'
    ]

    return concepts
