from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Initialize the chatbot with a unified name
chatbot = ChatBot('AD_NEXUS CampaignBot')

# Set up and train the chatbot with the English language corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Function to get a response from the chatbot
def get_chatbot_response(user_input):
    """
    Retrieves a response from the chatbot based on user input.

    Args:
        user_input (str): The user's message to the chatbot.

    Returns:
        str: The chatbot's response.
    """
    return chatbot.get_response(user_input)
