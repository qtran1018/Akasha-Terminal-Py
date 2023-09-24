from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv('OPEN_AI_API_KEY')

def chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = [{"role": "user", "content": prompt}],
            temperature = 0.7
        )
        response_dict = response.get("choices")
        if response_dict and len(response_dict) > 0:
            response = response_dict[0]['message']['content']
        return response
    except Exception as e:
        print(e)
        return str(e)
