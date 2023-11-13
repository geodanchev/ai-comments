import json
import openai
from helpers.config_helper import getOpenAIEndpoint, getOpenAIKey

openai.api_key = getOpenAIKey()
openai.api_base = getOpenAIEndpoint()
openai.api_type = "azure"
openai.api_version = "2023-05-15"

def test_prompt_with_chat_gpt():
    return get_feedback_temperament_and_category("The customer support was incredibly helpful, but the "
                                                 "product stopped working after just two weeks.")

def get_feedback_temperament_and_category(feedback):
    chatResult = prompt_with_chat_gpt(feedback,
                                "Analyze the following feedback text and determine both the "
                                "temperament (positive, neutral, or negative) and the category "
                                "(e.g., customer service, product quality, user experience), "
                                "and return json as a result")
    if is_satisfying(chatResult):
        return chatResult
    else:
        return  {
            "temperament": "error",
            "category": "error",
            "actualResult": chatResult,
        }

def is_satisfying(chatResult):
    try:
        message_json = json.loads(chatResult)
        if "temperament" in message_json and "category" in message_json:
            return True
        else:
            print("The JSON object structure is not as expected.")
            return False
    except json.JSONDecodeError:
        print("The message_content is not a valid JSON object.")
        return False
    
def prompt_with_chat_gpt(prompt, sysMessage):
    completion = openai.ChatCompletion.create(
        deployment_id="gpt-4",
        model="gpt-4",
        temperature=0.1,
        max_tokens=30,
        messages=[
            {"role": "system", "content": sysMessage},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content
