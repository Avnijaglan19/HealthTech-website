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
                  "You are a fitness assistant that creates workout plans. "
                  "ONLY use real YouTube video links from known fitness channels such as Athlean-X, FitnessBlender, or official exercise tutorial channels. "
                  "If you are not 100% sure the video is real and accurate, DO NOT include a link for that exercise. "
                  "Never invent or guess YouTube video IDs. "
                  "All links must be real, working YouTube URLs in full format like https://www.youtube.com/watch?v=VIDEO_ID. "
                  "If no valid video exists, leave the exercise without a link."  
                )
            },
                {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    return content if content is not None else ""