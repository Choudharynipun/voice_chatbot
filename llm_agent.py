import os
import openai
import time
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def query_llm(prompt: str):
    
    print("Preparing to send prompt to LLM...")
    print(f"Prompt: {prompt}")

    try:
        # Start measuring time
        start_time = time.time()

        # Send request to OpenAI ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change this to Together or Groq later
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # End measuring time
        end_time = time.time()

        # Calculate total time taken
        delay = end_time - start_time

        # Extract response text from the LLM output
        answer = response.choices[0].message.content
        print("LLM response received successfully.")
        print(f"Response Time (TTFT): {delay:.2f} seconds")
        print(f"Response: {answer}")

        return answer, delay

    except Exception as e:
        print("An error occurred while querying the LLM.")
        print("Error:", e)
        return "", 0.0
