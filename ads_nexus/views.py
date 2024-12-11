from django.shortcuts import render, redirect, get_object_or_404
from .models import Recommendation, Ad, AdSimulation, SocialMediaAccount, SocialMediaPlatform, AdCampaign, AdTargeting, AdPerformance, SocialShareAnalytics, UserDemographics, UserBehavior, AdPlatform
from .recommendation_engine import recommend_ads
from .simulation_engine import simulate_ad_performance
from .ai_tools import generate_creative_content
from .forms import AdCampaignForm, AdTargetingForm, PerformanceSimulationForm, AdContentForm, SchedulePostForm
from .ai_content_generator import generate_ad_copy
from social_django.models import UserSocialAuth
from .marketing_coach import get_marketing_advice
from .recommendation import recommend
from .performance_simulation import simulate_ad_performance, simulate_campaign_performance
from .creativity_boost import boost_creativity
from .chatbot import get_chatbot_response, AIChatbot, log_conversation
from .facebook_integration import create_facebook_campaign
from .google_ads_integration import create_google_ads_campaign
from .facebook_ads import FacebookAdManager
from .ai.content_recommendation import ContentRecommendationEngine
from .ai.performance_simulation import PerformanceSimulation
from .ai.creativity_booster import CreativityBooster
from .recommendations import recommend_ads
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot_handler import get_chatbot_response
import json
from .ad_targeting import dynamic_ad_targeting
from django.contrib.auth.decorators import login_required
from .performance_simulator import simulate_ad_performance
from .ad_integration import create_ad_on_platform
from .chatbot_service import get_chatbot_response

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

@login_required
def create_ad_campaign(request):
    if request.method == 'POST':
        form = AdCampaignForm(request.POST)
        if form.is_valid():
            # Save the campaign without committing to the database yet
            campaign = form.save(commit=False)
            campaign.user = request.user  # Associate the campaign with the logged-in user
            campaign.save()  # Save the campaign

            # Perform dynamic ad targeting based on the campaign details
            targeted_users = dynamic_ad_targeting(campaign)

            # Assuming you have a Many-to-Many field for users in the AdCampaign model
            campaign.targeted_users.set(targeted_users)  # Set the targeted users

            # Redirect to the success page or to the next step (like setting ads)
            return redirect('campaign_success')  # Redirect to a page that shows campaign success
        else:
            # Handle form errors
            return render(request, 'ads_nexus/create_ad_campaign.html', {'form': form})

    else:
        # Display an empty form for GET requests
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
    """
    Handles ad and campaign performance simulations based on user inputs or defaults.
    """
    if request.method == "POST":
        # Fetch input data from the form
        ad_spend = float(request.POST.get('ad_spend', 0))
        ctr = float(request.POST.get('ctr', 0))
        engagement_rate = float(request.POST.get('engagement_rate', 0))
        budget = float(request.POST.get('budget', 1000))  # Default campaign budget
        audience_size = int(request.POST.get('audience_size', 5000))  # Default audience size

        # Run ad performance simulation
        ad_performance = simulate_ad_performance(ad_spend, ctr, engagement_rate)
        clicks, engagements = ad_performance['clicks'], ad_performance['engagements']

        # Run campaign performance simulation
        campaign_performance = simulate_campaign_performance(budget, audience_size, engagement_rate)

        # Render results to the template
        return render(request, 'ads_nexus/performance_simulation_results.html', {
            'clicks': clicks,
            'engagements': engagements,
            'campaign_performance': campaign_performance,
        })

    # Render the input form page
    return render(request, 'ads_nexus/performance_simulation.html')

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

def content_recommendations(request):
    user_id = request.user.id  # Assuming user is logged in
    recommended_ads = generate_content_recommendations(user_id)

    return render(request, 'ads_nexus/content_recommendations.html', {'recommended_ads': recommended_ads})

# Initialize the AI Chatbot
chatbot = AIChatbot()

def chatbot_interface(request):
    user_message = ''
    chatbot_response = ''

    if request.method == "POST":
        user_message = request.POST['user_message']
        chatbot_response = chatbot.get_response(user_message)

    return render(request, 'ads_nexus/chatbot_interface.html', {
        'user_message': user_message,
        'chatbot_response': chatbot_response
    })

# Example access token and ad account ID (replace with actual values)
ACCESS_TOKEN = 'your_facebook_access_token'
AD_ACCOUNT_ID = 'your_ad_account_id'

# Initialize Facebook Ad Manager
fb_ad_manager = FacebookAdManager(ACCESS_TOKEN, AD_ACCOUNT_ID)

def create_facebook_ad(request):
    if request.method == 'POST':
        campaign_name = request.POST['campaign_name']
        adset_name = request.POST['adset_name']
        ad_name = request.POST['ad_name']
        targeting = request.POST['targeting']
        daily_budget = request.POST['daily_budget']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        # Create Campaign
        campaign = fb_ad_manager.create_campaign(campaign_name, 'CONVERSIONS')

        # Create Ad Set
        adset = fb_ad_manager.create_adset(
            campaign.get_id(),
            adset_name,
            targeting,
            daily_budget,
            start_time,
            end_time
        )

        # Assuming a pre-created creative ID for simplicity
        creative_id = 'your_creative_id'

        # Create Ad
        ad = fb_ad_manager.create_ad(adset.get_id(), ad_name, creative_id)

        return render(request, 'ads_nexus/ad_created.html', {
            'ad_id': ad.get_id(),
            'campaign_name': campaign_name,
            'adset_name': adset_name,
            'ad_name': ad_name,
        })
    return render(request, 'ads_nexus/create_ad.html')

# Example ad data (replace with real data from your database)
ad_data = {
    'ad_id': [1, 2, 3],
    'budget': [100, 200, 150],
    'targeting': [50, 60, 55],
    'schedule': [30, 40, 35]
}

# Initialize AI tools
content_rec_engine = ContentRecommendationEngine(ad_data)
performance_simulator = PerformanceSimulation(ad_data)
creativity_booster = CreativityBooster()

def ai_tools_dashboard(request):
    if request.method == 'POST':
        user_preferences = [
            request.POST['budget'],
            request.POST['targeting'],
            request.POST['schedule']
        ]

        # Get AI recommendations
        recommended_ad = content_rec_engine.recommend_content(user_preferences)

        # Simulate performance
        performance_score = performance_simulator.simulate_performance(
            request.POST['budget'],
            request.POST['targeting'],
            request.POST['schedule']
        )

        # Generate creative ad copy
        ad_copy = creativity_booster.generate_ad_copy(request.POST['ad_copy_input'])

        return render(request, 'ads_nexus/ai_dashboard_result.html', {
            'recommended_ad': recommended_ad,
            'performance_score': performance_score,
            'ad_copy': ad_copy
        })

    return render(request, 'ads_nexus/ai_dashboard.html')

def ad_detail(request, ad_id):
    ad = Ad.objects.get(id=ad_id)

    # Track social shares
    if request.GET.get('platform'):
        platform = request.GET['platform']
        share_analytics, created = SocialShareAnalytics.objects.get_or_create(ad=ad, platform=platform)
        share_analytics.share_count += 1
        share_analytics.save()

    # Get AI-powered ad recommendations for the user
    recommended_ads = recommend_ads(request.user.id)

    return render(request, 'ads_nexus/ad_detail.html', {
        'ad': ad,
        'recommended_ads': recommended_ads
    })

def analytics(request):
    analytics_data = SocialShareAnalytics.objects.all()
    return render(request, 'ads_nexus/analytics.html', {'analytics_data': analytics_data})

@login_required
@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        # If request is a standard POST (with form submission)
        if request.is_ajax():
            user_message = request.POST.get('message')
        else:
            # If request is in JSON format (API-based request)
            data = json.loads(request.body)
            user_message = data.get("message")

        if user_message:
            # Get the chatbot's response based on the user message
            chatbot_response = get_chatbot_response(user_message)

            # Log the conversation to the database
            log_conversation(request.user, user_message, chatbot_response)

            # Return the response as JSON
            return JsonResponse({"response": chatbot_response})
        else:
            return JsonResponse({"error": "No message provided"}, status=400)

    return render(request, 'chatbot.html')

def ad_performance(request, campaign_id):
    ad_campaign = get_object_or_404(AdCampaign, id=campaign_id)

    # Simulate performance data (this could be triggered periodically in production)
    ad_performance = simulate_ad_performance(ad_campaign)

    return render(request, 'ad_performance.html', {
        'ad_campaign': ad_campaign,
        'ad_performance': ad_performance
    })

def chatbot_view(request):
    return render(request, 'chatbot.html')

def get_chatbot_response_view(request):
    query = request.GET.get('query', '')
    response = get_chatbot_response(query)
    return JsonResponse({'response': response})

def manage_ad_campaign(request, campaign_id):
    ad_campaign = get_object_or_404(AdCampaign, id=campaign_id)
    platforms = AdPlatform.objects.all()

    if request.method == "POST":
        selected_platforms = request.POST.getlist('platforms')  # Get selected platforms from the form
        for platform_id in selected_platforms:
            platform = AdPlatform.objects.get(id=platform_id)
            create_ad_on_platform(ad_campaign, platform)  # Simulate ad creation on the platform

        return redirect('ad_performance', campaign_id=campaign_id)  # Redirect to performance page

    return render(request, 'manage_ad_campaign.html', {
        'ad_campaign': ad_campaign,
        'platforms': platforms
    })
