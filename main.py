import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

config=types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt
)

def main():
    parser = argparse.ArgumentParser(description="Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.verbose:
        print(f'User prompt: {args.user_prompt}')


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API key is missing")

    client = genai.Client(api_key=api_key)    
    messages: list[types.Content] = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        final = generate_content(client, messages, args.verbose)
        if final:
            print("Final response:")
            print(final)
            return
    print("Max iterations reached")
    sys.exit(1)

    
def generate_content(client: genai.Client, messages: list[types.Content], verbose: bool) -> str|None:
    response = client.models.generate_content(model = "gemini-2.5-flash", contents=messages, 
    config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions], temperature=0))
    if response.usage_metadata == None:
        raise RuntimeError('Metadata is missing')
    
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)
    
    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
        print('test')

    if not response.function_calls:        
        print("Response:")
        return response.text

    function_responses: list[types.Part] = []
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])

    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
