import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv("url/.env")

api_gemini = os.getenv('GEMINI_API_KEY')



def test_get_gemini_response():
    api_key = api_gemini
    prompt = "Explain the significance of the Turing Test in artificial intelligence."
    
    result = get_gemini_response(prompt, api_key)
    print(result)

def get_gemini_response(prompt, api_key):
    # Configure the API key
    genai.configure(api_key=api_key)

    # Initialize the model with default generation settings
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    print("RESPONSE FROM GEMINI")
    # Start a chat session
    chat_session = model.start_chat()

    # Send the prompt to the model
    response = chat_session.send_message(prompt)

    # Return the model's response text
    return response.text

# if __name__ == "__main__":
#     test_get_gemini_response()