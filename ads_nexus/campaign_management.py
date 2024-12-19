import facebook
from instabot import Bot
import tweepy

class CampaignManager:
    def __init__(self, facebook_token, instagram_username, instagram_password, twitter_keys):
        self.facebook_token = facebook_token
        self.instagram_username = instagram_username
        self.instagram_password = instagram_password
        self.twitter_keys = twitter_keys

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
