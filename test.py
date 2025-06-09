from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))




def chat_with_bot(prompt):
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {
          "role":"user",
          "content": prompt
      }
    ]
)
    return completion.choices[0].message.content.strip()

if __name__ == "__main__":
    while True :
        request = input('Enter Your question: ')
        if request.lower() == 'none':
            print('Thank You')
            break
        else :
            response = chat_with_bot(request)
            print("Chatbot:", response)


