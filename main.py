import os
import argparse
from dotenv import load_dotenv
from google import genai

parser = argparse.ArgumentParser(description="Agent")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("API key is missing")
client = genai.Client(api_key=api_key)

def main():
    response = client.models.generate_content(model = "gemini-2.5-flash" , contents=args.user_prompt)
    if response.usage_metadata == None:
        raise RuntimeError('Metadata is missing')
    else:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    print(response.text)

if __name__ == "__main__":
    main()
