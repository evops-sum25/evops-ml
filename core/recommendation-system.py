from typing import Dict, List, Optional, TypedDict, Union, Tuple
import numpy as np
from enum import Enum
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List


model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

# Embeddings should be obtained from the database
embeddings = ...

class ReactionType(Enum):
    GOOD = "good"
    NEUTRAL = "neutral"
    BAD = "bad"

# Subject to change
emoji_dict = {
    '❤️': ReactionType.GOOD,
    '🥰': ReactionType.GOOD,
    '😱': ReactionType.NEUTRAL,
    '👍': ReactionType.GOOD,
    '👎': ReactionType.BAD,
    '😇': ReactionType.NEUTRAL,
    '😭': ReactionType.NEUTRAL,
    '🔥': ReactionType.GOOD,
    '😐': ReactionType.BAD
}

def converted_emoji(emoji: str) -> List[ReactionType]:
    return list(emoji_dict[emoji])

# Subject to change
class EventInteraction(TypedDict):
    commented: bool
    upvoted: Optional[bool]
    attended: bool
    reactions: List[ReactionType]

class UserProfileBuilder:
    def __init__(self, weights_config: Optional[Dict] = None, lambda_param = 1):
        self.default_weights = {
            "commented": 1.3,
            "upvoted": {
                True: 2,     # Upvote
                False: -0.5, # Downvote
                None: 0      # No reaction
            },
            "attended": 2.0,
            "reactions": {
                ReactionType.GOOD: 1.2,
                ReactionType.NEUTRAL: 1,
                ReactionType.BAD: -0.8
            }
        }
        self.lambda_param = lambda_param
        self.weights = weights_config or self.default_weights

    def compute_weight(self, interaction: EventInteraction) -> float:
        total_weight = 0.0
        
        if interaction["commented"]:
            total_weight += self.weights["commented"]
        
        vote_key = interaction["upvoted"]
        total_weight += self.weights["upvoted"].get(vote_key, 0.0)

        if interaction["attended"]:
            total_weight += self.weights["attended"]
        
        for reaction in interaction["reactions"]:
            total_weight += self.weights["reactions"].get(reaction, 0.0)
            
        return total_weight

    def build_profile(
        self,
        interactions: List[EventInteraction], 
        event_embeddings: List[np.ndarray],
        return_components: bool = False
    ) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
        assert len(interactions) == len(event_embeddings)
        
        good_sum = np.zeros_like(event_embeddings[0])
        good_total_weight = 0.0
        bad_sum = np.zeros_like(event_embeddings[0])
        bad_total_weight = 0.0

        for i, emb in enumerate(event_embeddings):
            weight = self.compute_weight(interactions[i])
            
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
        
        if return_components:
            return combined_profile, good_profile, bad_profile
        
        return combined_profile

# def get_recommendations(user_id: int, k: int = 5) -> List[int]:
#     user_profile_vector = df_user_profiles.loc[df_user_profiles["user_id"] == user_id, "profile"].iloc[0]
    
#     seen_post_ids = df_users[df_users["user_id"] == user_id]["post_id"].unique()
#     unseen_posts = df_posts[~df_posts["post_id"].isin(seen_post_ids)].copy()

#     all_post_embeddings = np.vstack(unseen_posts["embedding"].values)

#     scores = cosine_similarity(
#         user_profile_vector.reshape(1, -1),
#         all_post_embeddings
#     ).flatten()
#     unseen_posts["score"] = scores

#     recommended_posts = unseen_posts.sort_values(by="score", ascending=False)

#     return recommended_posts.head(k)["post_id"].tolist()

# predict(user_profile, all_posts, amount_of_recommended) -> recommended_posts

class RecommendationSystem:
    def __init__(self):
        pass

    def predict(self, user_profile: np.ndarray, all_posts_embeddings: List[np.ndarray], n: int) -> List[int]:
        pass

    def update_profile(grouped):
        for user_id, group in grouped:
            interactions_list = []
            embeddings_list = []
            
            for _, row in group.iterrows():
                interaction = EventInteraction(
                    commented=row['commented'],
                    upvoted=row['upvoted'],
                    attended=row['attended'],
                    reactions=converted_emoji(row['reactions'])
                )
                
                post_emb = df_posts[df_posts['post_id'] == row['post_id']]['embedding']
                if post_emb is None:
                    continue
                post_emb = post_emb.iloc[0]
                
                interactions_list.append(interaction)
                embeddings_list.append(post_emb)
            
            if interactions_list:
                combined_emb = builder.build_profile(
                    interactions_list, 
                    embeddings_list
                )
                user_profiles[user_id] = combined_emb
            
            results.append({
                'user_id': user_id,
                'profile': combined_emb
            })
