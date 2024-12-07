from django.shortcuts import render
from .models import Recommendation
from .recommendation_engine import recommend_ads

def ad_recommendations(request):
    user_profile = request.user.userprofile  # Assumes user is logged in
    recommend_ads(user_profile.id)  # Generate recommendations

    recommendations = Recommendation.objects.filter(user=user_profile).order_by('-score')
    return render(request, 'ads_nexus/recommendations.html', {'recommendations': recommendations})
