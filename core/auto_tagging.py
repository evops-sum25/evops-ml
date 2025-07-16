from transformers import pipeline, AutoTokenizer
from typing import List, Generator
import unicodedata
import re
import emoji
import torch
import random


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

    def predict(self, event_description: str, tag_list: List = [], batch_size: int = 10) -> Generator[str, None, None]:
        '''
        Identifies relevant tags for an event description using zero-shot classification.
        Yields qualifying tags in batches as they become available

        Args:
            event_description (str): Text description of the event to classify
            tag_list: Custom tags (uses default if empty)
            batch_size: Processing chunk size

        Returns:
            Relevant tags meeting confidence threshold
        '''
        if len(tag_list) == 0:
            tag_list = self.tags
        random.shuffle(tag_list)
        event_description = self._preprocess_description(event_description)

        for i in range(0, len(tag_list), batch_size):
            batch = tag_list[i:i + batch_size]
            
            result = self.classifier(
                event_description,
                candidate_labels=batch,
                truncation=True,
                multi_label=True
            )
            
            for tag, score in zip(result['labels'], result['scores']):
                if score >= self.threshold:
                    yield tag
