import pandas as pd
import numpy as np
import json
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from .models import UserProfile, Ad, Recommendation


# Collaborative Filtering with Surprise
def collaborative_filtering_setup():
    """
    Sets up the collaborative filtering model using a dummy dataset.
    Returns the trained model and the unique ad IDs.
    """
    # Dummy dataset of user interactions with ads
    data = {
        'user_id': [1, 1, 1, 2, 2, 3, 3, 3],
        'ad_id': [1, 2, 3, 1, 4, 2, 3, 5],
        'rating': [5, 4, 3, 2, 5, 3, 4, 1],
    }
    df = pd.DataFrame(data)

    # Define the reader and load the data into Surprise format
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'ad_id', 'rating']], reader)

    # Split the data into training and test sets
    trainset, testset = train_test_split(data, test_size=0.2)

    # Train the SVD model
    model = SVD()
    model.fit(trainset)

    return model, df['ad_id'].unique()


def get_recommendations(user_id, model, all_ads, n_recommendations=5):
    """
    Generates collaborative filtering-based recommendations for a user.

    Args:
        user_id (int): The user's ID.
        model: The trained collaborative filtering model.
        all_ads (array): Array of all unique ad IDs.
        n_recommendations (int): Number of recommendations to return.

    Returns:
        list: Top N recommended ad IDs.
    """
    predictions = [
        (ad, model.predict(user_id, ad).est) for ad in all_ads
    ]
    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:n_recommendations]


# Content-Based Filtering
def recommend_ads(user_profile_id):
    """
    Generates content-based ad recommendations for a user based on their preferences.

    Args:
        user_profile_id (int): The ID of the user's profile.

    Returns:
        list: A list of recommendations with ads and scores.
    """
    try:
        # Fetch user profile and their preferences
        user_profile = UserProfile.objects.get(id=user_profile_id)
        user_preferences = json.loads(user_profile.preferences)
    except UserProfile.DoesNotExist:
        return []

    # Fetch all ads
    ads = Ad.objects.all()

    recommendations = []

    for ad in ads:
        # Calculate a relevance score based on user preferences and ad categories
        score = sum(
            weight for preference, weight in user_preferences.items()
            if preference in ad.category.lower()
        )

        # Only recommend ads with a score > threshold
        if score > 0.5:  # Adjust threshold as needed
            recommendations.append({"ad": ad, "score": score})

    # Save recommendations to the database
    for recommendation in recommendations:
        Recommendation.objects.create(
            user=user_profile,
            ad=recommendation["ad"],
            score=recommendation["score"],
        )

    return recommendations


# Unified Recommendation Function
def generate_recommendations(user_id, use_collaborative=True, n_recommendations=5):
    """
    Combines collaborative and content-based filtering to generate recommendations.

    Args:
        user_id (int): The user's ID.
        use_collaborative (bool): Whether to use collaborative filtering.
        n_recommendations (int): Number of recommendations to return.

    Returns:
        list: Combined or specific recommendations.
    """
    if use_collaborative:
        # Collaborative Filtering
        model, all_ads = collaborative_filtering_setup()
        return get_recommendations(user_id, model, all_ads, n_recommendations)
    else:
        # Content-Based Filtering
        return recommend_ads(user_id)
