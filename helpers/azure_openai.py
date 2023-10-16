import openai
import sys

if len(sys.argv) < 3:
    raise Exception(
        "Please provide the needed arguments. Readme.txt for more info")
key = sys.argv[1]
if len(key) != 32:
    raise Exception(f"key should be with 32 chars but it is {len(key)}")

openai.api_key = key
openai.api_base = "https://copstesting.openai.azure.com"
openai.api_type = "azure"
openai.api_version = "2023-05-15"


def test_prompt_with_chat_gpt():
    return get_feedback_temperament_and_category("The customer support was incredibly helpful, but the "
                                                 "product stopped working after just two weeks.")


def get_feedback_temperament_and_category(feedback):
    return prompt_with_chat_gpt(feedback,
                                "Analyze the following feedback text and determine both the "
                                "temperament (positive, neutral, or negative) and the category "
                                "(e.g., customer service, product quality, user experience), "
                                "and return json as result like this:")


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