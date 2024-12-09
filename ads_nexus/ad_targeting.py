import random
from .models import UserDemographics, UserBehavior, AdCampaign

# Function to perform dynamic targeting for an ad campaign
def dynamic_ad_targeting(campaign):
    # Filter users based on the campaign's targeting criteria
    eligible_users = []

    for user in UserDemographics.objects.all():
        # Get user's demographics and behaviors
        behavior = UserBehavior.objects.get(user=user.user)

        # Apply targeting criteria
        if (campaign.target_age_range and not age_in_range(user.age, campaign.target_age_range)):
            continue
        if (campaign.target_gender and user.gender != campaign.target_gender):
            continue
        if (campaign.target_location and user.location != campaign.target_location):
            continue
        if (campaign.target_interests and not any(interest in campaign.target_interests for interest in behavior.interests)):
            continue

        eligible_users.append(user.user)

    # Simulate ad targeting success (random selection for demonstration)
    targeted_users = random.sample(eligible_users, k=min(10, len(eligible_users)))  # Limit to top 10 users
    return targeted_users

# Function to check if age is within the target range
def age_in_range(user_age, target_age_range):
    min_age, max_age = map(int, target_age_range.split('-'))
    return min_age <= user_age <= max_age
