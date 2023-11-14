import json
from openai import AzureOpenAI
from helpers.config_helper import getOpenAIEndpoint, getOpenAIKey

client = AzureOpenAI(azure_endpoint=getOpenAIEndpoint(),
                     api_key=getOpenAIKey(),
                     api_version="2023-05-15")

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
    completion = client.chat.completions.create(
        model="gpt-4",
        temperature=0.7,
        messages=[
            {"role": "system", "content": sysMessage},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

def summarize_transcript(transcript):
    return prompt_with_chat_gpt(transcript,
                                "Analyze the following transcription and return short summarization as bullet points")