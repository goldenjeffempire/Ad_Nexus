def get_marketing_advice(campaign_data):
    # Simple rule-based advice based on the campaign's performance
    if campaign_data['engagement_rate'] < 10:
        return "Your campaign engagement is low. Try experimenting with more engaging content or targeting a different audience."
    elif campaign_data['engagement_rate'] > 50:
        return "Your campaign is performing well! Keep up the great work and consider increasing your budget to reach a wider audience."
    else:
        return "Your campaign is doing okay, but there’s room for improvement. Consider optimizing your targeting strategy."
