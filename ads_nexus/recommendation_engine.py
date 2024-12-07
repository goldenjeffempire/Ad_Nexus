import json
from .models import UserProfile, Ad, Recommendation

def recommend_ads(user_profile_id):
    # Fetch user profile and their preferences
    try:
        user_profile = UserProfile.objects.get(id=user_profile_id)
        user_preferences = json.loads(user_profile.preferences)
    except UserProfile.DoesNotExist:
        return []

    # Fetch all ads
    ads = Ad.objects.all()

    recommendations = []

    for ad in ads:
        # Calculate a relevance score based on user preferences and ad category
        score = 0
        for preference, weight in user_preferences.items():
            if preference in ad.category.lower():
                score += weight

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
