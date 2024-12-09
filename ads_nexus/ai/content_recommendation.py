import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

class ContentRecommendationEngine:
    def __init__(self, ad_data):
        self.ad_data = ad_data
        self.label_encoder = LabelEncoder()
        self.ad_data['ad_id'] = self.label_encoder.fit_transform(self.ad_data['ad_id'])

    def train_model(self):
        # Basic collaborative filtering model using TensorFlow
        ad_ids = self.ad_data['ad_id'].values
        features = self.ad_data.drop(columns='ad_id').values
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(features.shape[1],)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model.fit(features, ad_ids, epochs=5)

    def recommend_content(self, user_preferences):
        # Generate content recommendations for a user
        user_vector = np.array(user_preferences).reshape(1, -1)
        recommendation = self.model.predict(user_vector)
        recommended_ad_id = self.label_encoder.inverse_transform([np.argmax(recommendation)])
        return recommended_ad_id
