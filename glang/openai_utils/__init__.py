from dynaconf import settings
import openai

openai.organization = "org-GWrcbj6eKedKfWRYyhCxclf6"
openai.api_key = settings.OPENAI_KEY
openai_client = openai
__all__ = ["openai_client"]
