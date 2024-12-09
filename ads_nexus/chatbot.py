from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Initialize the chatbot
chatbot = ChatBot('AD_NEXUS ChatBot')

# Set up the chatbot's trainer
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Function to get chatbot's response
def get_response(message):
    return chatbot.get_response(message)
