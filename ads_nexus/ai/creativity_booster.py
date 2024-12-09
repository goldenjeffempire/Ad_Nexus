from transformers import pipeline

class CreativityBooster:
    def __init__(self):
        self.generator = pipeline('text-generation', model='gpt2')

    def generate_ad_copy(self, input_text):
        response = self.generator(input_text, max_length=50, num_return_sequences=1)
        return response[0]['generated_text']
