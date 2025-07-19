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
