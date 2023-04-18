"""CLI interface for glang project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""

from phrase_getter import (
    build_prompt,
    send_prompt_to_openai,
    extract_phrases_from_completion,
)
import json


def main():  # pragma: no cover
    prompt = build_prompt(["losung", "eklaren"], num_phrases=3)
    print(prompt)
    completion = send_prompt_to_openai(prompt)
    print(completion)
    with open("/tmp/response.json", "w") as f:
        json.dump(completion, f, indent=2)
    phrases = extract_phrases_from_completion(completion)
    print(phrases)


if __name__ == "__main__":
    main()
