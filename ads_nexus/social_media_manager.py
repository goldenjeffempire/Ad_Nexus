class SocialMediaManager:
    def __init__(self, facebook_manager, twitter_manager, instagram_manager, tiktok_manager):
        self.facebook_manager = facebook_manager
        self.twitter_manager = twitter_manager
        self.instagram_manager = instagram_manager
        self.tiktok_manager = tiktok_manager

    def create_ad_on_all_platforms(self, ad_params, tweet_text, instagram_image_url, instagram_caption, tiktok_ad_params):
        # Create Facebook Ad
        facebook_ad = self.facebook_manager.create_ad(ad_params['ad_account_id'], ad_params)

        # Create Twitter Ad
        twitter_ad = self.twitter_manager.create_tweet(tweet_text)

        # Create Instagram Ad
        instagram_ad = self.instagram_manager.create_instagram_post(instagram_image_url, instagram_caption)

        # Create TikTok Ad
        tiktok_ad = self.tiktok_manager.create_tiktok_ad(tiktok_ad_params)

        return {
            'facebook': facebook_ad,
            'twitter': twitter_ad,
            'instagram': instagram_ad,
            'tiktok': tiktok_ad
        }
