from django.shortcuts import render, redirect, get_object_or_404
from .models import Recommendation, Ad, AdSimulation, SocialMediaAccount, SocialMediaPlatform
from .recommendation_engine import recommend_ads
from .simulation_engine import simulate_ad_performance
from .ai_tools import generate_creative_content

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

def ai_creativity_booster(request):
    if request.method == "POST":
        # Generate AI-powered content
        generated_content = generate_creative_content()
    else:
        generated_content = None

    return render(request, 'ads_nexus/ai_creativity_booster.html', {
        'generated_content': generated_content
    })

def social_media_dashboard(request):
    accounts = SocialMediaAccount.objects.filter(user=request.user)
    platforms = SocialMediaPlatform.objects.all()

    return render(request, 'ads_nexus/social_media_dashboard.html', {
        'accounts': accounts,
        'platforms': platforms,
    })


def connect_social_media_account(request, platform_id):
    platform = get_object_or_404(SocialMediaPlatform, id=platform_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        access_token = request.POST.get('access_token')  # Simulated connection
        SocialMediaAccount.objects.create(
            user=request.user,
            platform=platform,
            username=username,
            access_token=access_token
        )
        return redirect('social_media_dashboard')

    return render(request, 'ads_nexus/connect_social_media.html', {'platform': platform})
