from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class AIChatbot:
    def __init__(self):
        # Initialize the chatbot with a unified name
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
        return self.chatbot.get_response(user_input)
