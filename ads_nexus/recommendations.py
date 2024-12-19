import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder
from .models import Ad, UserBehavior
from collections import counter

def recommend_content(user):
    # Fetch the user's interactions
    interactions = Interaction.objects.filter(user=user)

    # Collect the content IDs that the user has interacted with
    interacted_content_ids = [interaction.content.id for interaction in interactions]

    # Fetch content that is similar (using tags for content-based filtering)
    similar_content = Content.objects.filter(tags__overlap=interacted_content_ids)

    # For collaborative filtering (simple version):
    # Find other users with similar interactions
    similar_users = Interaction.objects.filter(content_id__in=interacted_content_ids).exclude(user=user).values('user').distinct()

    recommended_content = []
    for similar_user in similar_users:
        user_interactions = Interaction.objects.filter(user_id=similar_user['user'])
        for interaction in user_interactions:
            if interaction.content.id not in interacted_content_ids:
                recommended_content.append(interaction.content)

    # Combine content-based and collaborative recommendations (simplified)
    combined_recommendations = list(set(recommended_content + list(similar_content)))

    return combined_recommendations

# Sample AI model to recommend ads based on user behavior (content-based filtering)

def train_model():
    ads = Ad.objects.all()  # Get all ads
    behaviors = UserBehavior.objects.all()  # Get user behaviors

    # Simplified feature extraction (e.g., ad category and user engagement)
    ad_categories = [ad.category for ad in ads]
    user_engagement = [behavior.engagement_score for behavior in behaviors]

    # Encode categories
    encoder = LabelEncoder()
    ad_categories_encoded = encoder.fit_transform(ad_categories)

    # Model features (for simplicity, using a basic concatenation of category and engagement)
    features = np.array(list(zip(ad_categories_encoded, user_engagement)))

    # Neural network model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(features.shape[1],)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')  # Predict user interest in ads
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(features, np.random.rand(len(ads)), epochs=10)  # Dummy target values for now
    return model

# Function to predict recommendations for a user
def recommend_ads(user_id):
    # Fetch user behavior data (e.g., past ad engagements, views)
    user_behavior = UserBehavior.objects.filter(user_id=user_id)

    # Get ad categories and user engagement data
    user_engagement = [behavior.engagement_score for behavior in user_behavior]
    ad_categories = [behavior.ad.category for behavior in user_behavior]

    # Process the data
    encoder = LabelEncoder()
    ad_categories_encoded = encoder.fit_transform(ad_categories)
    features = np.array(list(zip(ad_categories_encoded, user_engagement)))

    # Use trained AI model to recommend ads
    model = train_model()  # Using the trained model (or load from disk if pre-trained)
    predictions = model.predict(features)

    # Sort predictions to suggest the most relevant ads
    recommended_ads = sorted(zip(predictions, user_behavior), key=lambda x: x[0], reverse=True)
    return [ad[1].ad for ad in recommended_ads[:5]]  # Top 5 recommended ads
