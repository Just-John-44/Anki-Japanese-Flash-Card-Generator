# test_sentence_generator.py
# Created: 6/18/2026
# Last Edited: 6/18/2026
# Author: John Wesley Thompson

import pytest

from src.sentence_generator import OpenAISentenceGenerator 
from src.sentence_generator import PROMPT_HEADER 

class FakeClient:
    '''Fake OpenAI client used for injection in tests'''
    def chat(self, *args, **kwargs):
        return "fake response"


def test_init_with_injected_client():
    '''Tests that the class is initialized with a test-client and test-model'''
    fake_client = FakeClient()
    gen = OpenAISentenceGenerator(client=fake_client, model="test-model")

    assert isinstance(gen.client, FakeClient)
    assert gen.model == "test-model"


def test_missing_api_key(monkeypatch):
    '''Tests that the initialization of the class fails if the OpenAI API key isn't found'''
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError):
        OpenAISentenceGenerator()