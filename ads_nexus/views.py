from django.shortcuts import render, redirect, get_object_or_404
from .models import Recommendation, Ad, AdSimulation, SocialMediaAccount, SocialMediaPlatform, AdCampaign, AdTargeting, AdPerformance, SocialShareAnalytics, UserDemographics, UserBehavior, AdPlatform, EngagementInsight, ScheduledPost, AdAnalytics, ContentRecommendation, SocialMediaAccount, SocialMediaPost, EngageMetric, AdPerformanceSimulation, CrossPlatformCampaign, Platform, SocialMediaAPI
from .recommendation_engine import recommend_ads
from .simulation_engine import simulate_ad_performance
from .ai_tools import generate_creative_content
from .forms import AdCampaignForm, AdTargetingForm, PerformanceSimulationForm, AdContentForm, SchedulePostForm, SocialMediaAccountForm
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
from .campaign_management import CampaignManager
from .social_media_manager import SocialMediaManager, FacebookAdManager, TwitterAdManager, InstagramAdManager, TikTokAdManager

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
    simulate_ad_performance(ad_campaign)

    # Fetch performance data for the specific campaign
    performance_data = AdPerformance.objects.filter(campaign_id=campaign_id)

    # Calculate totals and averages
    total_clicks = sum([p.clicks for p in performance_data])
    total_impressions = sum([p.impressions for p in performance_data])
    average_engagement_rate = (
        sum([p.engagement_rate for p in performance_data]) / len(performance_data)
        if performance_data else 0
    )
    total_conversions = sum([p.conversions for p in performance_data])

    context = {
        'ad_campaign': ad_campaign,
        'performance_data': performance_data,
        'total_clicks': total_clicks,
        'total_impressions': total_impressions,
        'average_engagement_rate': average_engagement_rate,
        'total_conversions': total_conversions,
    }

    return render(request, 'ad_performance.html', context)

def manage_social_media_accounts(request):
    user = request.user
    accounts = SocialMediaAccount.objects.filter(user=user)

    if request.method == 'POST':
        form = SocialMediaAccountForm(request.POST)
        if form.is_valid():
            form.instance.user = user
            form.save()
            return redirect('manage_social_media_accounts')
    else:
        form = SocialMediaAccountForm()

    return render(request, 'manage_social_media_accounts.html', {'accounts': accounts, 'form': form})def manage_social_media_accounts(request):
    user = request.user
    accounts = SocialMediaAccount.objects.filter(user=user)

    if request.method == 'POST':
        form = SocialMediaAccountForm(request.POST)
        if form.is_valid():
            form.instance.user = user
            form.save()
            return redirect('manage_social_media_accounts')
    else:
        form = SocialMediaAccountForm()

    return render(request, 'manage_social_media_accounts.html', {'accounts': accounts, 'form': form})
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

def link_social_media_account(request):
    if request.method == 'POST':
        form = SocialMediaAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('social_media_accounts')
    else:
        form = SocialMediaAccountForm()
    return render(request, 'link_social_media_account.html', {'form': form})

def social_media_accounts(request):
    accounts = SocialMediaAccount.objects.filter(user=request.user)
    return render(request, 'social_media_accounts.html', {'accounts': accounts})

def view_engagement_insights(request, account_id):
    account = SocialMediaAccount.objects.get(id=account_id)
    insights = EngagementInsight.objects.filter(social_media_account=account)
    return render(request, 'engagement_insights.html', {'account': account, 'insights': insights})

def schedule_post(request, account_id):
    account = SocialMediaAccount.objects.get(id=account_id)

    if request.method == 'POST':
        form = ScheduledPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('social_media_accounts')
    else:
        form = ScheduledPostForm(initial={'social_media_account': account})
    return render(request, 'schedule_post.html', {'form': form, 'account': account})

def view_ad_analytics(request, campaign_id):
    campaign = AdCampaign.objects.get(id=campaign_id)
    analytics_data = AdAnalytics.objects.filter(ad_campaign=campaign).order_by('-date')
    return render(request, 'view_ad_analytics.html', {'campaign': campaign, 'analytics_data': analytics_data})

def generate_report(request, campaign_id):
    campaign = AdCampaign.objects.get(id=campaign_id)
    analytics_data = AdAnalytics.objects.filter(ad_campaign=campaign)
    total_impressions = sum([data.impressions for data in analytics_data])
    total_clicks = sum([data.clicks for data in analytics_data])
    total_conversions = sum([data.conversions for data in analytics_data])

    report = {
        'campaign_name': campaign.campaign_name,
        'total_impressions': total_impressions,
        'total_clicks': total_clicks,
        'total_conversions': total_conversions,
        'click_through_rate': (total_clicks / total_impressions) * 100 if total_impressions else 0,
        'conversion_rate': (total_conversions / total_impressions) * 100 if total_impressions else 0,
    }

    return render(request, 'generate_report.html', {'report': report})

def content_recommendations(request):
    """
    Generate and render content recommendations for the logged-in user.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered content recommendations page.
    """
    user = request.user

    # Generate recommendations using a unified function
    recommendations = generate_recommendations(user)

    # Context dictionary for rendering the template
    context = {
        'recommendations': recommendations
    }

    return render(request, 'content_recommendations.html', context)

def manage_social_media_accounts(request):
    user = request.user
    accounts = SocialMediaAccount.objects.filter(user=user)

    if request.method == 'POST':
        form = SocialMediaAccountForm(request.POST)
        if form.is_valid():
            form.instance.user = user
            form.save()
            return redirect('manage_social_media_accounts')
    else:
        form = SocialMediaAccountForm()

    return render(request, 'manage_social_media_accounts.html', {'accounts': accounts, 'form': form})

def engagement_insights(request):
    user = request.user
    posts = SocialMediaPost.objects.filter(account__user=user)

    engagement_data = []
    for post in posts:
        engagement = EngagementMetric.objects.get(post=post)
        engagement_data.append({
            'post': post,
            'engagement': engagement
        })

    return render(request, 'engagement_insights.html', {'engagement_data': engagement_data})

def performance_simulation(request):
    user = request.user
    posts = SocialMediaPost.objects.filter(account__user=user)

    performance_data = []
    for post in posts:
        try:
            performance = AdPerformanceSimulation.objects.get(post=post)
            performance.simulate_performance()
            performance_data.append({
                'post': post,
                'performance': performance
            })
        except AdPerformanceSimulation.DoesNotExist:
            performance_data.append({
                'post': post,
                'performance': None
            })

    return render(request, 'performance_simulation.html', {'performance_data': performance_data})

def create_campaign(request):
    """
    Handle the creation of social media campaigns and posting ads to selected platforms.
    """
    platforms = Platform.objects.all()

    if request.method == 'POST':
        # Fetch campaign details from the request
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        selected_platforms = request.POST.getlist('platforms')
        message = request.POST.get('message')
        image_path = request.FILES.get('image_path', None)  # Image for Instagram
        video_path = request.FILES.get('video_path', None)  # Video for TikTok

        # Social media credentials (to be replaced with environment variables or secure storage)
        facebook_token = 'your_facebook_access_token'
        instagram_username = 'your_instagram_username'
        instagram_password = 'your_instagram_password'
        twitter_keys = (
            'your_twitter_api_key',
            'your_twitter_api_secret',
            'your_twitter_access_token',
            'your_twitter_access_token_secret'
        )
        tiktok_credentials = 'your_tiktok_credentials'  # Add TikTok credentials (or cookies/login method)

        # Initialize the CampaignManager with credentials
        manager = CampaignManager(
            facebook_token, instagram_username, instagram_password, twitter_keys, tiktok_credentials
        )

        # Create the campaign in the database
        campaign = CrossPlatformCampaign.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )

        # Add the selected platforms to the campaign
        for platform_id in selected_platforms:
            platform = get_object_or_404(Platform, id=platform_id)
            campaign.platforms.add(platform)

        campaign.save()

        # Attempt to post to the selected platforms
        try:
            for platform_id in selected_platforms:
                platform = get_object_or_404(Platform, id=platform_id)

                if platform.name.lower() == 'facebook':
                    manager.post_to_facebook(message)
                elif platform.name.lower() == 'instagram':
                    if not image_path:
                        return JsonResponse({'status': 'error', 'message': 'Image is required for Instagram posts'})
                    manager.post_to_instagram(message, image_path.temporary_file_path())  # Access temporary file path
                elif platform.name.lower() == 'twitter':
                    manager.post_to_twitter(message)
                elif platform.name.lower() == 'tiktok':
                    if not video_path:
                        return JsonResponse({'status': 'error', 'message': 'Video is required for TikTok posts'})
                    manager.post_to_tiktok(message, video_path.temporary_file_path())  # Access temporary file path
                else:
                    return JsonResponse({'status': 'error', 'message': f'Invalid platform: {platform.name}'})

            return JsonResponse({'status': 'success', 'message': f'Campaign and ads successfully posted to selected platforms.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to post ad: {str(e)}'})

    return render(request, 'create_campaign.html', {'platforms': platforms})

def view_campaigns(request):
    campaigns = CrossPlatformCampaign.objects.all()
    return render(request, 'view_campaigns.html', {'campaigns': campaigns})

def integrate_api(request):
    if request.method == 'POST':
        platform = request.POST.get('platform')
        api_key = request.POST.get('api_key')
        api_secret = request.POST.get('api_secret')
        access_token = request.POST.get('access_token')
        access_token_secret = request.POST.get('access_token_secret', '')

        # Save API credentials to the database
        SocialMediaAPI.objects.create(
            platform=platform,
            api_key=api_key,
            api_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        return redirect('view_api_settings')

    return render(request, 'integrate_api.html')

def view_api_settings(request):
    api_settings = SocialMediaAPI.objects.all()
    return render(request, 'view_api_settings.html', {'api_settings': api_settings})

def create_social_media_ad(request):
    if request.method == 'POST':
        # Fetch ad details from the request
        ad_params = request.POST.get('ad_params')
        tweet_text = request.POST.get('tweet_text')
        instagram_image_url = request.POST.get('instagram_image_url')
        instagram_caption = request.POST.get('instagram_caption')
        tiktok_ad_params = request.POST.get('tiktok_ad_params')

        # Initialize platform managers with credentials (example)
        facebook_manager = FacebookAdManager(access_token='FB_ACCESS_TOKEN', app_id='FB_APP_ID', app_secret='FB_APP_SECRET')
        twitter_manager = TwitterAdManager(api_key='TWITTER_API_KEY', api_secret_key='TWITTER_API_SECRET_KEY', access_token='TWITTER_ACCESS_TOKEN', access_token_secret='TWITTER_ACCESS_TOKEN_SECRET')
        instagram_manager = InstagramAdManager(access_token='INSTAGRAM_ACCESS_TOKEN', user_id='INSTAGRAM_USER_ID')
        tiktok_manager = TikTokAdManager(access_token='TIKTOK_ACCESS_TOKEN', app_id='TIKTOK_APP_ID')

        # Initialize Social Media Manager
        social_media_manager = SocialMediaManager(
            facebook_manager,
            twitter_manager,
            instagram_manager,
            tiktok_manager
        )

        # Create the ad across platforms
        ad_response = social_media_manager.create_ad_on_all_platforms(
            ad_params,
            tweet_text,
            instagram_image_url,
            instagram_caption,
            tiktok_ad_params
        )

        return JsonResponse(ad_response)

    return render(request, 'create_ad.html')
