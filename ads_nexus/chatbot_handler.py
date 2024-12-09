import os
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

# Set up Dialogflow credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/dialogflow-service-account-file.json"

# Define chatbot interaction function
def get_chatbot_response(text, user_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path('your-project-id', user_id)

    # Create a text input object
    text_input = dialogflow.TextInput(text=text, language_code='en')
    query_input = dialogflow.QueryInput(text=text_input)

    # Send the query to Dialogflow
    response = session_client.detect_intent(session=session, query_input=query_input)

    return response.query_result.fulfillment_text  # Return the response text
