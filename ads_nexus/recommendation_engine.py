# recommendation_engine.py
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import LabelEncoder
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from .models import UserProfile, Ad, Recommendation
import json

# Load and preprocess user behavior data
def load_data(file_path='user_behavior.csv'):
    """Loads and preprocesses user behavior data."""
    data = pd.read_csv(file_path)

    # Encode categorical data (ad_category)
    label_encoder = LabelEncoder()
    data['ad_category_encoded'] = label_encoder.fit_transform(data['ad_category'])

    return data, label_encoder

# Build and train a simple neural network for content-based filtering
def train_content_based_model(data):
    """Trains a content-based recommendation model."""
    X = data[['user_id', 'ad_category_encoded']]
    y = data['interaction_score']

    model = Sequential([
        Dense(128, activation='relu', input_dim=X.shape[1]),
        Dense(64, activation='relu'),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=10, batch_size=32)

    return model

# Collaborative Filtering setup
def collaborative_filtering_setup():
    """Sets up the collaborative filtering model using a dummy dataset."""
    data = {
        'user_id': [1, 1, 1, 2, 2, 3, 3, 3],
        'ad_id': [1, 2, 3, 1, 4, 2, 3, 5],
        'rating': [5, 4, 3, 2, 5, 3, 4, 1],
    }
    df = pd.DataFrame(data)

    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'ad_id', 'rating']], reader)

    trainset, testset = train_test_split(data, test_size=0.2)

    model = SVD()
    model.fit(trainset)

    return model, df['ad_id'].unique()

# Get recommendations using collaborative filtering
def get_collaborative_recommendations(user_id, model, all_ads, n_recommendations=5):
    """Generates collaborative filtering-based recommendations."""
    predictions = [
        (ad, model.predict(user_id, ad).est) for ad in all_ads
    ]
    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:n_recommendations]

# Get recommendations using content-based filtering
def get_content_based_recommendations(user_id, data, model, label_encoder, top_n=5):
    """Generates content-based ad recommendations."""
    ads = data['ad_id'].unique()
    ad_predictions = []

    for ad in ads:
        ad_category = data[data['ad_id'] == ad]['ad_category_encoded'].iloc[0]
        prediction = model.predict([[user_id, ad_category]])
        ad_predictions.append((ad, prediction[0][0]))

    recommended_ads = sorted(ad_predictions, key=lambda x: x[1], reverse=True)
    return recommended_ads[:top_n]

# Content-Based Filtering with Django models
def recommend_ads_with_user_profile(user_profile_id):
    """Generates content-based recommendations using user preferences."""
    try:
        user_profile = UserProfile.objects.get(id=user_profile_id)
        user_preferences = json.loads(user_profile.preferences)
    except UserProfile.DoesNotExist:
        return []

    ads = Ad.objects.all()
    recommendations = []

    for ad in ads:
        score = sum(
            weight for preference, weight in user_preferences.items()
            if preference in ad.category.lower()
        )
        if score > 0.5:
            recommendations.append({"ad": ad, "score": score})

    for recommendation in recommendations:
        Recommendation.objects.create(
            user=user_profile,
            ad=recommendation["ad"],
            score=recommendation["score"],
        )

    return recommendations

# Unified recommendation engine
def generate_recommendations(user_id, data, label_encoder, use_collaborative=True, n_recommendations=5):
    """Generates recommendations using collaborative or content-based filtering."""
    if use_collaborative:
        model, all_ads = collaborative_filtering_setup()
        return get_collaborative_recommendations(user_id, model, all_ads, n_recommendations)
    else:
        content_model = train_content_based_model(data)
        return get_content_based_recommendations(user_id, data, content_model, label_encoder, n_recommendations)

# Example usage (ensure data file exists and models are set up properly):
# data, label_encoder = load_data()
# recommendations = generate_recommendations(user_id=1, data=data, label_encoder=label_encoder, use_collaborative=False)
