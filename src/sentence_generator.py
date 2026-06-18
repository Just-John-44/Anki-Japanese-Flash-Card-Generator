# John Wesley Thompson
# Created: 8/12/2025
# Last Edited: 6/18/2026
# sentence_generator.py

# import card_file_manager as cfm
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

# PROMPT_HEADER = '''
# Hello! I'm going to provide you with a list of words in Japanese.\n
# For each word, please generate 2 example sentences and tell me the\n
# formality level of the word. For the formality, I want to know if\n
# the word is 丁寧語, 尊敬語, casual, etc. Please do this in the\n
# following format: \n\n
# 1. word (the second word would be "2. word", and so on)\n
# sentence 1\n
# sentence 2\n
# (formality)\n\n
# please do not stop generating sentences until you have made them\n
# for every word. I'm certain that this is the desired format.\n\n
# Here is the list, and thank you!:\n
# '''
PROMPT_HEADER = '''
I'm going to provide you a list of words in Japanese.\n
For each word, please generate 2 example sentences and if applicable,
tell me if the word belongs to any of the following categories/tags:

Register:
Casual, Neutral, Polite, Formal, Very Formal, Honorific, Humble, Business,
Literary, Old-fashioned, Slang, Masculine, Feminine, Childish, Vulgar

Context/Domain:
Academic, Professional, Legal, Medical, Technical, Scientific, Computing/IT,
Engineering, Financial, Government, Military, Religious, Historical, Educational,
News, Internet, Social Media, Gaming, Anime/Manga, Sports, Travel, Food, Family,
Romance, Daily Life

Frequency:
Common, Uncommon

Situational:
Mostly Spoken, Mostly Written, Conversational, Public Speaking, Customer Service,
Email, Texting, Telephone, Workplace, Classroom

please do so in the following json format:\n
[
    "word1": {
        "s1": "insert first generated sentence here for word 1.",
        "s2": "insert second generated sentence here for word 1.",
        "tags": "tag1・tag2・tag3・..."
    },
    "word2": {
        ...
        ...
        ...
    },
    "word..."
]
'''

load_dotenv()

class OpenAISentenceGenerator:
    def __init__(self, client=None, model: str="gpt-4o-mini"):
        self.model = model

        if client is not None:
            self.client = client
            return

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY")

        self.client = OpenAI(api_key=api_key)

    def __del__(self):
        self.client.close()

    def generateSentences(self, prompt_header, vocab):
        vocab = ['\u3000'.join(word) if word[0] else word[1] for word in vocab]
        vocab_text = '\n'.join(vocab)

        full_prompt = prompt_header + vocab_text
        chat_completion = self.client.chat.completions.create(
            model = self.model,
            messages = [
            {
                "role": "system",
                "content": "Return output in json only. No explanation. No markdown"
            },
            {
                "role": "user",
                "content": full_prompt
            }]
        )

        response_text = chat_completion.choices[0].message.content

        data = json.loads(response_text)

        # this makes a list of strings of 2 example sentences
        new_sentences = []
        for word, entry in data.items():
            new_sentences.append(entry["s1"] + ' ' + entry["s2"])

        return new_sentences


if __name__ == "__main__":

    gen = OpenAISentenceGenerator()
    # cfm.initConfigFile()
    # file_manager = cfm.CardFileManager()
    # model = file_manager.getConfig("OPENAI_MODEL")

    vocab = (("図書館", "としょかん"), ("割り勘", "わりかん"), ("", "テスト"))
    gen.generateSentences(PROMPT_HEADER, vocab)