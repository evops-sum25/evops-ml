import requests
from typing import List, Union, TypedDict


class APIError(TypedDict):
    error: str


class TextTranslation(TypedDict):
    translatedText: List[str]


class DetectedLanguage(TypedDict):
    language: str


class Language(TypedDict):
    code: str
    name: str


class LanguageList(TypedDict):
    availableLanguages: List[Language]


class Translator:
    def __init__(self) -> None:
        self.translate_url = f"http://31.59.41.8:5000/translate"
        self.detect_url = f"http://31.59.41.8:5000/detect"
        self.languages_url = f"http://31.59.41.8:5000/languages"


    def translate(
        self,
        text: Union[str, List[str]],
        target_lang: str,
        source_lang: str = "auto",
    ) -> Union[TextTranslation, APIError]:
        """
        Translates a string or a list of strings.

        Args:
            - text: The text or list of texts to translate.
            - target_lang: The language code to translate to (e.g., "en", "ru").
            - source_lang: The source language code. Defaults to auto detection.

        Returns:
            - A dictionary containing either `translatedText` with a list of strings on success
                or `error` with its description on failure.
        """

        try:
            payload = {
                "q": text,
                "source": source_lang,
                "target": target_lang,
                "format": "text"
            }
            response = requests.post(url=self.translate_url, json=payload)
            response.raise_for_status()

            data = response.json()
            translated_data = data["translatedText"]

            if isinstance(text, str):
                return {"translatedText": [translated_data]}
            else:
                return {"translatedText": translated_data}
        except requests.exceptions.HTTPError as e:
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


    def detect_language(self, text: str) -> Union[DetectedLanguage, APIError]:
        """
        Detects the language of a given text string.

        Args:
            - text: The text to analyze.

        Returns:
            - A dictionary containing either `language` with the detected language code (e.g., "en", "ru") on success
                or `error` with its description on failure.
        """

        try:
            payload = {
                "q": text
            }
            response = requests.post(url=self.detect_url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            detected_language = data[0]["language"]

            return {"language": detected_language}
        except requests.exceptions.HTTPError as e:
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


    def get_languages(self) -> Union[LanguageList, APIError]:
        """
        Fetches the list of languages supported by the server.

        Returns:
            - A dictionary containing either `availableLanguages`
                with the list of dictionaries with `code` and `name` of the available languages
                or `error` with its description.
        """

        try:
            response = requests.get(url=self.languages_url)
            response.raise_for_status()

            data = response.json()
            available_languages: List[Language] = [
                {"code": language["code"], "name": language["name"]}
                for language in data
            ]

            return {"availableLanguages": available_languages}
        except requests.exceptions.HTTPError as e:
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
