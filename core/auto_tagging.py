from transformers import pipeline, AutoTokenizer
from typing import List
import unicodedata
import re
import emoji
import torch


class ZeroShotTagger:
    def __init__(self, threshold=0.8):
        '''
        Initializing the tag classifier

        Args:
            threshold: Confidence threshold for tags
        '''
        self.threshold = threshold

        self.tokenizer = AutoTokenizer.from_pretrained('sileod/deberta-v3-base-tasksource-nli', model_max_length=512)

        self.classifier = pipeline(
            "zero-shot-classification",
            model='sileod/deberta-v3-base-tasksource-nli',
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )

        # Should be obtained from the database
        self.tags = [
            # --- Primary Event & Opportunity Types ---
            "Workshop",
            "Lecture",
            "Seminar",
            "Talk",
            "Conference",
            "Forum",
            "Hackathon",
            "Olympiad",
            "Contest",
            "Festival",
            "Job Fair",
            "Master Class",
            "Club Meeting",
            "Ball",
            "Concert",
            "Party",
            "Quiz",
            "Game",
            "Internship",
            "Volunteering",
            # --- Common Topics ---
            "Programming",
            "Artificial Intelligence",
            "Computer Science",
            "Machine Learning",
            "Data Science",
            "Cybersecurity",
            "Robotics",
            "Science",
            "Mathematics",
            "Physics",
            "Business",
            "Startups",
            "Design",
            "Art",
            "Music",
            "Dance",
            "Sports",
            "Language Learning"
        ]

    def _preprocess_description(self, event_description: str) -> str:
        '''
        Performs text normalization and cleaning.
        Removes emojis, non-text elements, URLs, and non-standard characters.
        Supports Unicode normalization, HTML tag removal, and whitespace reduction.

        Args:
            text: Raw input string to be processed

        Returns:
            str: Normalized and cleaned text
        '''
        event_description = emoji.replace_emoji(event_description, replace='')
        event_description = unicodedata.normalize('NFKC', event_description)
        event_description = re.sub(r'<[^>]+>', '', event_description)
        event_description = re.sub(r'https?://\S+|www\.\S+', '', event_description)
        event_description = re.sub(r'[^\w\s.,!?;:()"\'-]', '', event_description)
        event_description = re.sub(r'\s+', ' ', event_description).strip()
        return event_description

    def predict(self, event_description: str, tag_list: List = []) -> List[str]:
        '''
        Identifies relevant tags for an event description using zero-shot classification.
        Returns tags above the specified threshold.

        Args:
            event_description (str): Text description of the event to classify

        Returns:
            list: List of tag filtered by threshold,
                sorted by descending confidence (order from classifier output)
        '''
        if len(tag_list) == 0:
            tag_list = self.tags
        # Preprocessing a description
        event_description = self._preprocess_description(event_description)

        result = self.classifier(
            event_description,
            candidate_labels=tag_list,
            truncation=True,
            multi_label=True
        )

        # Filtering tags by threshold
        relevant_tags = [
            tag
            for tag, score in zip(result['labels'], result['scores'])
            if score >= self.threshold
        ]

        return relevant_tags
