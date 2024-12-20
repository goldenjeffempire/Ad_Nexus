from .models import ChatHistory
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Simple rule-based AI chatbot response function
def get_chatbot_response(user_message):
    responses = {
        "hello": "Hi there! How can I assist you today?",
        "help": "Sure! I can help you with campaign creation, ad targeting, and more. What would you like to know?",
        "ad campaign": "You can create an ad campaign by filling in the details like target age range, gender, budget, etc. Would you like to proceed?",
        "goodbye": "Goodbye! Feel free to reach out anytime.",
    }

    # Check if the message matches predefined keywords
    user_message = user_message.lower()
    response = responses.get(user_message, "Sorry, I didn't understand that. Can you rephrase?")

    return response

# Function to log the conversation
def log_conversation(user, user_message, chatbot_response):
    ChatHistory.objects.create(user=user, message=user_message, response=chatbot_response)

class AIChatbot:
    def __init__(self):
        # Initialize the chatbot with a unified name and logic adapters
        self.chatbot = ChatBot(
            'AD_NEXUS CampaignBot',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            logic_adapters=[
                'chatterbot.logic.BestMatch',
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.TimeLogicAdapter'
            ],
            database_uri='sqlite:///chatbot_db.sqlite3'
        )

        # Set up the trainer and train the chatbot with the English language corpus
        self.trainer = ChatterBotCorpusTrainer(self.chatbot)
        self.trainer.train('chatterbot.corpus.english')

    def get_response(self, user_input):
        """
        Retrieves a response from the chatbot based on user input.

        Args:
            user_input (str): The user's message to the chatbot.

        Returns:
            str: The chatbot's response.
        """
        # First, check if the message matches predefined responses
        rule_based_response = get_chatbot_response(user_input)

        # If the rule-based response is a fallback, use ChatterBot's AI response
        if "Sorry, I didn't understand that" in rule_based_response:
            ai_response = self.chatbot.get_response(user_input)
            response = ai_response.text  # Extract text from ChatterBot response
        else:
            response = rule_based_response

        return response

    def log_and_respond(self, user, user_message):
        """
        Logs the conversation and returns the chatbot's response.

        Args:
            user: The user instance making the request.
            user_message (str): The user's message to the chatbot.

        Returns:
            str: The chatbot's response.
        """
        # Get response from AI chatbot
        chatbot_response = self.get_response(user_message)

        # Log the conversation
        log_conversation(user, user_message, chatbot_response)

        return chatbot_response


# chatbot.py
import os
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

# Load credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(
    'path_to_your_service_account_file.json'
)

# Initialize Dialogflow session client
def detect_intent(text_input, session_id="12345"):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path('your-project-id', session_id)

    # Create the text input for the query
    text_input = dialogflow.TextInput(text=text_input, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    # Detect intent
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text
