import json
import os
import re

from openai import OpenAI
from dotenv import load_dotenv


# Loads environment variables from a .env file into the system's environment variables
load_dotenv()

# Retrieves the value of the environment variable "OPENAI_KEY" and assigns it to the variable api_key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

ALLOWED_EQUIPMENT = [
    "barbell",
    "bench",
    "bodyweight",
    "cable machine",
    "dumbbells",
    "kettlebell",
    "resistance band",
    "treadmill",
    "weight plates",
]


def normalize_equipment_name(value):
    cleaned = str(value or "").strip().lower()
    if not cleaned:
        return None

    aliases = {
        "dumbbell": "dumbbells",
        "dumbbells": "dumbbells",
        "kettlebells": "kettlebell",
        "kettlebell": "kettlebell",
        "resistance bands": "resistance band",
        "resistance band": "resistance band",
        "cable_machine": "cable machine",
        "cable-machine": "cable machine",
        "weight plate": "weight plates",
        "weight plates": "weight plates",
        "body weights": "bodyweight",
        "bodyweight": "bodyweight",
    }

    return aliases.get(cleaned, cleaned)


def parse_equipment_response(raw_text):
    text = (raw_text or "").strip()
    if not text:
        return ["bodyweight"]

    cleaned = re.sub(r"```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    cleaned = cleaned.strip("`\n \t")

    if not cleaned:
        return ["bodyweight"]

    if cleaned.lower() in {"bodyweight", "no equipment detected", "none", "no equipment", "no listed equipment visible"}:
        return ["bodyweight"]

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.findall(r'"([^"]+)"', cleaned)
        if match:
            parsed = match
        else:
            parsed = [cleaned]

    if isinstance(parsed, str):
        parsed = [parsed]

    if not isinstance(parsed, list):
        parsed = [str(parsed)]

    normalized = []
    seen = set()
    for item in parsed:
        normalized_name = normalize_equipment_name(item)
        if normalized_name in ALLOWED_EQUIPMENT and normalized_name not in seen:
            normalized.append(normalized_name)
            seen.add(normalized_name)

    if not normalized:
        return ["bodyweight"]

    return normalized

# ================================================================================================
#
# generateWorkoutPlan(prompt):
# Purpose: This function takes in a prompt as a string, sends it to the OpenAI API to generate a 
# workout plan based on the prompt, and returns the generated workout plan as a string
# 
# ================================================================================================

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

# ================================================================================================
#
# create_file(file_path):
# Purpose: This function takes in a file path, creates a file using the OpenAI Files API, and 
# returns the file ID. 
# 
# ================================================================================================
def createFile(file_path):
  with open(file_path, "rb") as file_content:
    result = client.files.create(
        file=file_content,
        purpose="vision",
    )
    return result.id


# ================================================================================================
#
# generate_equipment(image_path):
# Purpose: This function takes in the file path of an image, creates a file using the OpenAI 
# Files API, and then generates a response from the OpenAI API
# 
# ================================================================================================

def generateEquipment(image_path): 
    file_id = createFile(image_path)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "You are an equipment detection assistant. Analyze " \
                 "the image and identify only equipment from this allowed list:" \
                 "barbell, bench, bodyweight, cable machine, dumbbells, kettlebell, resistance band, " \
                 "treadmill, weight plates. " \
                 "Return only valid JSON in this exact format: [\"barbell\", \"bench\"] " \
                 "or [\"bodyweight\"]. " \
                 "If no listed equipment is visible, return [\"bodyweight\"]. " \
                 "Do not include any explanation, markdown fences, or extra text."
                },
                {
                    "type": "input_image",
                    "file_id": file_id,
                },
            ],
        }], # type: ignore
    )

    return parse_equipment_response(response.output_text or "")