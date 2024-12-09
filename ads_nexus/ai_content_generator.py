import openai

openai.api_key = 'your_openai_api_key'

def generate_ad_copy(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or a model that fits your use case
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        ad_copy = response.choices[0].text.strip()
        return ad_copy
    except Exception as e:
        return f"Error generating content: {str(e)}"
