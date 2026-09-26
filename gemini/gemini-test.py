from google import genai
from google.genai.types import HttpOptions, ModelContent, Part, UserContent
import os
from pathlib import Path

def load_env_file(env_path=".env"):
    env_file = Path(env_path)

    if not env_file.exists():
        raise FileNotFoundError("Environment file not found. This file contains API Key")

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip().strip('"').strip("'")

load_env_file()
api_key = os.environ.get("GOOGLE_GEMINI_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_GEMINI_API_KEY is missing in the environment file.")

#from dotenv import load_dotenv
#load_dotenv()
#api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

#print(f"API Key: {api_key}")


def return_generated_content_2() -> str:
    client = genai.Client(api_key=api_key)
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input="Explain how AI works in a few words"
    )
    print(interaction.output_text)
    return interaction.output_text

def return_generated_content_1() -> str:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        #model="gemini-3.8-flash",
        model="gemini-2.0-flash",
        contents="Tell me a story.",
    )
    print(response.text)
    return response.text


if __name__ == "__main__":
    #return_generated_content_1()
    return_generated_content_2()
    
# Google’s Gemini API gemini-3.8-flash, the current Free Tier limit appears to be:
# 20 requests/day (RPD)
# 5 RPM (requests per minute)
# Google’s rate-limit system also uses requests per minute (RPM) and input tokens per minute (TPM), but Google does not publish a fixed RPM/TPM number for every model on the public documentation page; your project’s actual limits are shown in AI Studio. 
# 1,048,576 input-token context limit
# 65,536 maximum output tokens 
# https://ai.google.dev/gemini-api/docs/rate-limits?utm_source=chatgpt.com
