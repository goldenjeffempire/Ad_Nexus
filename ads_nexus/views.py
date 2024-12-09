from django.shortcuts import render, redirect, get_object_or_404
from .models import Recommendation, Ad, AdSimulation, SocialMediaAccount, SocialMediaPlatform, AdCampaign, AdTargeting, AdCampaign, AdPerformance
from .recommendation_engine import recommend_ads
from .simulation_engine import simulate_ad_performance
from .ai_tools import generate_creative_content
from .forms import AdCampaignForm, AdTargetingForm, PerformanceSimulationForm, AdContentForm, SchedulePostForm
from .ai_content_generator import generate_ad_copy
from social_django.models import UserSocialAuth
from .marketing_coach import get_marketing_advice
from .recommendation import recommend
from .performance_simulation import simulate_campaign_performance
from .creativity_boost import boost_creativity
from .chatbot import get_chatbot_response
from .facebook_integration import create_facebook_campaign
from .google_ads_integration import create_google_ads_campaign

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

def create_ad_campaign(request):
    if request.method == 'POST':
        form = AdCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = request.user
            campaign.save()
            return redirect('set_ad_targeting', campaign_id=campaign.id)
    else:
        form = AdCampaignForm()

    return render(request, 'ads_nexus/create_ad_campaign.html', {'form': form})


def set_ad_targeting(request, campaign_id):
    campaign = get_object_or_404(AdCampaign, id=campaign_id)
    if request.method == 'POST':
        form = AdTargetingForm(request.POST)
        if form.is_valid():
            targeting = form.save(commit=False)
            targeting.campaign = campaign
            targeting.save()
            return redirect('campaign_dashboard')
    else:
        form = AdTargetingForm()

    return render(request, 'ads_nexus/set_ad_targeting.html', {'form': form, 'campaign': campaign})

def simulate_performance(request, campaign_id):
    campaign = get_object_or_404(AdCampaign, id=campaign_id)
    if request.method == 'POST':
        form = PerformanceSimulationForm(request.POST)
        if form.is_valid():
            ad_spend = form.cleaned_data['ad_spend']
            revenue = form.cleaned_data['revenue']
            performance, created = AdPerformance.objects.get_or_create(campaign=campaign)
            performance.impressions = form.cleaned_data['impressions']
            performance.clicks = form.cleaned_data['clicks']
            performance.calculate_ctr()
            performance.calculate_cpc(ad_spend)
            performance.calculate_roi(revenue)
            performance.save()

            return render(request, 'ads_nexus/performance_result.html', {'performance': performance})
    else:
        form = PerformanceSimulationForm()

    return render(request, 'ads_nexus/simulate_performance.html', {'form': form, 'campaign': campaign})

def generate_ad_content(request):
    ad_copy = None
    if request.method == 'POST':
        form = AdContentForm(request.POST)
        if form.is_valid():
            campaign_description = form.cleaned_data['campaign_description']
            ad_copy = generate_ad_copy(campaign_description)
    else:
        form = AdContentForm()

    return render(request, 'ads_nexus/generate_ad_content.html', {'form': form, 'ad_copy': ad_copy})

def social_media_dashboard(request):
    if request.user.is_authenticated:
        social_accounts = UserSocialAuth.objects.filter(user=request.user)
        return render(request, 'ads_nexus/social_media_dashboard.html', {'social_accounts': social_accounts})
    else:
        return render(request, 'ads_nexus/login.html')

def engagement_insights(request):
    if request.user.is_authenticated:
        # Simulated insights
        posts = [
            {"title": "Ad Campaign 1", "likes": 150, "comments": 32},
            {"title": "Ad Campaign 2", "likes": 240, "comments": 45},
        ]
        return render(request, 'ads_nexus/engagement_insights.html', {'posts': posts})
    else:
        return render(request, 'ads_nexus/login.html')

def schedule_post(request):
    if request.method == 'POST':
        form = SchedulePostForm(request.POST)
        if form.is_valid():
            # Simulate scheduling the post
            # Here, add your logic to schedule the post
            return render(request, 'ads_nexus/schedule_post_confirmation.html', {'form': form})
    else:
        form = SchedulePostForm()

    return render(request, 'ads_nexus/schedule_post.html', {'form': form})

def marketing_coach(request):
    # Simulate campaign data
    campaign_data = {'engagement_rate': 15}  # Example engagement rate
    advice = get_marketing_advice(campaign_data)

    return render(request, 'ads_nexus/marketing_coach.html', {'advice': advice})

def content_recommendation(request):
    user_id = 'user1'  # Example user ID, this can be dynamically fetched
    recommendations = recommend(user_id)
    return render(request, 'ads_nexus/recommendations.html', {'recommendations': recommendations})

def performance_simulation(request):
    budget = 1000  # Example budget in USD
    audience_size = 5000  # Example audience size
    engagement_rate = 0.3  # Example engagement rate (30%)

    performance = simulate_campaign_performance(budget, audience_size, engagement_rate)
    return render(request, 'ads_nexus/performance_simulation.html', {'performance': performance})

def creativity_boost(request):
    ad_content = "Amazing product at a great price!"  # Example ad content
    suggestion = boost_creativity(ad_content)
    return render(request, 'ads_nexus/creativity_boost.html', {'suggestion': suggestion})

def chatbot_interaction(request):
    user_input = request.GET.get('user_input', '')  # Get user input from GET request
    if user_input:
        response = get_chatbot_response(user_input)
    else:
        response = "Hi, I am your campaign assistant. How can I help you today?"

    return render(request, 'ads_nexus/chatbot_interaction.html', {'response': response})

def manage_campaigns(request):
    if request.method == 'POST':
        platform = request.POST.get('platform')
        campaign_name = request.POST.get('campaign_name')
        budget = float(request.POST.get('budget'))

        if platform == 'Facebook':
            campaign = create_facebook_campaign(campaign_name, 'CONVERSIONS', 'PAUSED')
            return render(request, 'ads_nexus/campaign_created.html', {'campaign': campaign})

        elif platform == 'Google Ads':
            google_campaign = create_google_ads_campaign('your_customer_id', campaign_name, budget)
            return render(request, 'ads_nexus/campaign_created.html', {'google_campaign': google_campaign})

    return render(request, 'ads_nexus/manage_campaigns.html')

from django.shortcuts import render
from .recommendation_engine import generate_content_recommendations

def content_recommendations(request):
    user_id = request.user.id  # Assuming user is logged in
    recommended_ads = generate_content_recommendations(user_id)

    return render(request, 'ads_nexus/content_recommendations.html', {'recommended_ads': recommended_ads})
