"""
Glang helps users learn german vocabulary. The user enters words they've revcently learned, and glang
returns phrases using those words, which will later be turned into voice. 
The phrases are generated by sending a prompt to OpenAI's GPT-3 API, which returns a list of phrases.
"""
from typing import List
from dataclasses import dataclass
import re
from openai_utils import openai_client
import json
from dynaconf import settings

print(settings.as_dict())


@dataclass
class Phrase:
    german: str
    english: str
    phrase: str


def build_prompt(words: List[str], current_level="b1", num_phrases=10):
    """
    Builds a prompt for GPT-3 to generate phrases based on the words

    """
    word_bullets = "\n".join([f"- {word}" for word in words])
    prompt = f""" The user wants to practice their German vocabulary. 
    They've recently learned the following words. For each word below, generate a phrase in German using that word
    You can use different variants of the word, but try to use each word at least once.
    Try to use verbs in both plural and singular (e.g. du, sie, ihr, wir, ihr, sie)

    {word_bullets}

    Start each phrase with the word, in all caps. Then write the phrase in german. End with the translation in english in parantheses.
    For example "LOSUNG: Die Losung ist, dass wir nicht aufgeben. (The solution is that we don't give up.)"
    Don't use a list format, don'treturn numbers or bullets. Instead seperate each phrase with a new line

    Make {num_phrases} phrases for each word.
    Use german appropriate for a {current_level} speaker.
    """
    return prompt


splitter_reg = re.compile(r"(?P<phrase>.+): (?P<german>.+) \((?P<english>.+)\)")


def extract_phrase_from_response(response_text: str) -> Phrase:
    """
    Response texts are lines that start each with the word, in all caps. Then  the phrase in german and end with the translation in english in parantheses.
    For example "LOSUNG: Die Losung ist, dass wir nicht aufgeben. (The solution is that we don't give up.)"
    It is xtracted using named capture groups in a  regex
    """
    capture = splitter_reg.match(response_text)
    if capture is None:
        print(response_text)
        raise ValueError(f"Could not extract phrase from {response_text}")
    return Phrase(**capture.groupdict())


def send_prompt_to_openai(prompt: str):
    completion = openai_client.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        stop=["STOP"],
        temperature=0,
        max_tokens=settings.MAX_OPENAI_TOKENS,
    )
    return completion


def extract_first_completion(completion):
    # check if the number of compeltion tokens is gte to our max setting
    if completion.usage.completion_tokens >= settings.MAX_OPENAI_TOKENS:
        return completion.choices[0].text + ")"
    else:
        return completion.choices[0].text


def extract_phrases_from_completion(completion) -> List[Phrase]:
    response_text = extract_first_completion(completion)
    phrases = [
        extract_phrase_from_response(line)
        for line in response_text.strip().splitlines()
    ]
    return phrases
