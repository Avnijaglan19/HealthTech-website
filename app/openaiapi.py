import os
from openai import OpenAI
from dotenv import load_dotenv


# Loads environment variables from a .env file into the system's environment variables
load_dotenv()

# Retrieves the value of the environment variable "OPENAI_KEY" and assigns it to the variable api_key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

def generateWorkoutPlan(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # lightweight + cheap model
        messages=[
            {
                "role": "system",
                "content": (
                  "You are a strict fitness assistant. "
                  "You MUST include EXACTLY ONE YouTube link for EVERY exercise. "
                  "Each exercise must follow this format:\n\n"
                  "Exercise Name:\n"
                  "https://www.youtube.com/watch?v=VIDEO_ID\n\n"
                  "Do NOT skip any exercises. "
                  "Do NOT write explanations instead of links. "
                  "Do NOT include text without a link."  
                )
            },
                {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    return content if content is not None else ""