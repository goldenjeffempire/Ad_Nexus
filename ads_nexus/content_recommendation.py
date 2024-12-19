def generate_recommendations(user):
    # Example: Recommend ads based on the user's recent clicks and interests
    recent_campaigns = AdCampaign.objects.filter(user_interactions__user=user).order_by('-user_interactions__timestamp')[:5]

    recommendations = []
    for campaign in recent_campaigns:
        score = calculate_recommendation_score(user, campaign)
        recommendations.append({
            'ad_campaign': campaign,
            'score': score
        })
    
    return recommendations

def calculate_recommendation_score(user, campaign):
    # Example: Calculate score based on past interactions (simplified)
    clicks = campaign.user_interactions.filter(user=user).count()
    return clicks * 1.5  # Simplified score calculation based on clicks
