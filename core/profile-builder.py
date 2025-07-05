from typing import Optional, List, Dict
import numpy as np


class UserProfileBuilder:
    """
    Builds a personalized user profile vector based on event interactions.
    Supports weighted aggregation of positive/negative interactions with normalization.

    Key Requirements:
        - Interaction dictionary keys must match weights configuration:
            * Top-level keys (e.g., 'upvoted', 'commented') must exist in self.weights
            * Reaction categories must exist in self.weights['reactions']

    Example interaction record:
    {
        'commented': True,
        'upvoted': False,
        'downvoted': True,
        'attended': True,
        'reactions': {
            'GOOD': 3,
            'NEUTRAL': 1,
            'BAD': 0
        }
    }
    
    Attributes:
        default_weights_config: Default weights for interaction types
        weights: Active weights configuration (custom or default)
        lambda_param: Scaling factor for negative interactions
    
    Methods:
        _compute_weight: Calculates interaction weight for a single event
        build_profile: Aggregates event embeddings into normalized user profile
    """

    # Subject to augment and change
    default_weights_config = {
        "commented": 1.3,
        "upvoted": 3,
        'downvoted': -5,
        "attended": 2.0,
        "reactions": {
            "GOOD": 1.2,
            "NEUTRAL": 0,
            "BAD": -0.8
        }
    }

    def __init__(self, weights_config: Optional[Dict] = None, lambda_param = 1):
        """
        Initializes profile builder with weights configuration

        Args:
            weights_config: Custom weights for interaction types
                Structure: {
                    "interaction_type": float_weight,
                    "reactions": {"REACTION_TYPE": float_weight}
                }
            lambda_param: Scaling factor for negative influence

        Precondition:
            Keys in weights_config (except 'reactions') must correspond to top-level keys 
            used in interaction dictionaries. Reaction categories must match keys in 
            weights_config['reactions'].
        """
        self.lambda_param = lambda_param
        self.weights = weights_config or self.default_weights_config

    def _compute_weight(self, interaction: Dict) -> float:
        """
        Computes aggregated weight for a single event interaction

        Args:
            interaction: Event interaction record with structure:
                {
                    "interaction_type": bool,
                    "reactions": {"REACTION_CATEGORY": count}
                }

        Returns:
            float: Computed interaction weight
        
        Note:
            - Requires key alignment between interaction keys and self.weights:
                * Top-level keys (except 'reactions') must exist in self.weights
                * Reaction categories must exist in self.weights['reactions']
            - Processes boolean interactions (e.g. upvoted=True)
            - Sums reaction weights by category counts
            - Reactions categories: GOOD/BAD/NEUTRAL
        """
        total_weight = 0.0
        for action, weight in interaction.items():
            if action == 'reactions':
                continue
            if weight:
                total_weight += self.weights[action]

        for type, amount in interaction['reactions'].items():
            total_weight += amount * self.weights['reactions'][type] 

        return total_weight

    def build_profile(
        self,
        interactions: List[Dict], 
        event_embeddings: List[np.ndarray]
    ) -> np.ndarray:
        """
        Builds normalized user profile from interaction history

        Args:
            interactions: List of interaction records per event
            event_embeddings: Corresponding event embedding vectors

        Returns:
            np.ndarray: Normalized profile vector
            
        Processing:
            1. Separates positive/negative interactions
            2. Computes weighted average vectors:
                - good_profile: Positive interactions cluster
                - bad_profile: Negative interactions cluster
            3. Combines: good_profile - lambda*bad_profile
            4. Applies L2 normalization
        
        Note:
            - Requires equal length of interactions and embeddings
            - Zero-weight interactions are ignored
            - Returns zero-vector when no valid interactions
        """
        good_sum = np.zeros_like(event_embeddings[0])
        good_total_weight = 0.0
        bad_sum = np.zeros_like(event_embeddings[0])
        bad_total_weight = 0.0

        for i, emb in enumerate(event_embeddings):
            weight = self._compute_weight(interactions[i])
            if weight > 0:
                good_sum += weight * emb
                good_total_weight += weight
            elif weight < 0:
                abs_weight = abs(weight)
                bad_sum += abs_weight * emb
                bad_total_weight += abs_weight
        
        good_profile = good_sum / good_total_weight if good_total_weight > 0 else good_sum
        bad_profile = bad_sum / bad_total_weight if bad_total_weight > 0 else bad_sum
        
        combined_profile = good_profile - self.lambda_param * bad_profile
        
        combined_profile_norm = np.linalg.norm(combined_profile)
        if combined_profile_norm > 0:
            combined_profile /= combined_profile_norm
        
        return combined_profile
