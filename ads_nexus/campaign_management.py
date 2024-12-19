import facebook
from instabot import Bot
import tweepy
from TikTokApi import TikTokApi

class CampaignManager:
    def __init__(self, facebook_token, instagram_username, instagram_password, twitter_keys, tiktok_credentials):
        self.facebook_token = facebook_token
        self.instagram_username = instagram_username
        self.instagram_password = instagram_password
        self.twitter_keys = twitter_keys
        self.tiktok_credentials = tiktok_credentials  # Credentials for TikTok (API key, secret, etc.)

    def post_to_facebook(self, message):
        graph = facebook.GraphAPI(self.facebook_token)
        post = graph.put_object(parent_object='me', connection_name='feed', message=message)
        return post

    def post_to_instagram(self, message, image_path):
        bot = Bot()
        bot.login(username=self.instagram_username, password=self.instagram_password)
        bot.upload_photo(image_path, caption=message)

    def post_to_twitter(self, message):
        api_key, api_secret, access_token, access_token_secret = self.twitter_keys
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(message)

    def post_to_tiktok(self, message, video_path):
        """
        This method will post content to TikTok.
        Assumes the video is in the correct format (e.g., mp4).
        """
        try:
            # Initialize the TikTokApi client
            api = TikTokApi.get_instance()

            # TikTok credentials could be handled via cookies or login details (for now, we assume no login is needed)
            # Alternatively, for account-based posting, you can authenticate using the tiktok_credentials

            # Example: Posting video to TikTok
            upload_response = api.upload_video(video_path, description=message)

            if upload_response:
                print(f"Video posted successfully to TikTok: {upload_response}")
                return upload_response
            else:
                raise Exception("Failed to upload video to TikTok")

        except Exception as e:
            print(f"Error posting to TikTok: {str(e)}")
            raise Exception(f"Error posting to TikTok: {str(e)}")
