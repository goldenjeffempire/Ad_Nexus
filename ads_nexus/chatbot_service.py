from .models import AIChatbot

def get_chatbot_response(query):
    # Check if the question exists in the chatbot database
    try:
        response = AIChatbot.objects.get(question__icontains=query)
        return response.answer
    except AIChatbot.DoesNotExist:
        return "I'm sorry, I couldn't understand your question. Could you try rephrasing it?"
