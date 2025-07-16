import re
import emoji
import unicodedata
from sentence_transformers import SentenceTransformer
import numpy as np

class EventEmbedder:
    """
    A text embedding generator.
    
    This class handles preprocessing of event descriptions and generates semantic embeddings
    using a multilingual sentence transformer model.
    """
    def __init__(self):
        """
        Initializes the embedding model.
        
        Loads the 'paraphrase-multilingual-mpnet-base-v2' transformer that produces
        768-dimensional embeddings.
        """
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

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
    
    def get_embedding(self, event_description: str) -> np.ndarray:
        """
        Generates a semantic embedding vector for the processed event description.
        
        Args:
            event_description: Raw text description of an event

        Returns:
            np.ndarray: 768-dimensional numpy array representing the semantic embedding
        """
        return self.model.encode(self._preprocess_description(event_description))
