from django.shortcuts import render, get_object_or_404
from .models import Recommendation, Ad, AdSimulation
from .recommendation_engine import recommend_ads
from .simulation_engine import simulate_ad_performance

def ad_recommendations(request):
    user_profile = request.user.userprofile  # Assumes user is logged in
    recommend_ads(user_profile.id)  # Generate recommendations

    recommendations = Recommendation.objects.filter(user=user_profile).order_by('-score')
    return render(request, 'ads_nexus/recommendations.html', {'recommendations': recommendations})

def ad_simulation(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    # Run simulation
    simulation = simulate_ad_performance(ad.id)

    # Fetch previous simulations for the same ad
    previous_simulations = AdSimulation.objects.filter(ad=ad).order_by('-created_at')

    return render(request, 'ads_nexus/ad_simulation.html', {
        'ad': ad,
        'simulation': simulation,
        'previous_simulations': previous_simulations,
    })
