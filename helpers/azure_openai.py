from openai import AzureOpenAI
from helpers.config_helper import getOpenAIEndpoint, getOpenAIKey
from tiktoken import encoding_for_model

client = AzureOpenAI(azure_endpoint=getOpenAIEndpoint(),
                     api_key=getOpenAIKey(),
                     api_version="2023-05-15")

def split_text_into_token_chunks(text, max_tokens, model):

    encoding = encoding_for_model(model)
    tokenized_text = encoding.encode(text)
    token_chunks = []
    current_chunk = []
    print(f'total number of tokens in this request is {len(tokenized_text)}')

    for token in tokenized_text:
        current_chunk.append(token)
        if len(current_chunk) >= max_tokens:
            joined_chunk = encoding.decode(current_chunk[:-1])  # Exclude the last token
            token_chunks.append(joined_chunk)
            current_chunk = [token] # Start a new chunk with the last token

    # Include any remaining tokens in the last chunk
    if current_chunk:
        token_chunks.append(encoding.decode(current_chunk))

    return token_chunks


def summarize_long_text(text, prompt, max_tokens=4096, model="gpt-4", temperature=0.7):
    token_chunks = split_text_into_token_chunks(text, max_tokens - 100, model)
    print(f'chunks based on maximum number of tokens = {max_tokens}')
    summaries = ""
    cnt = 0
    for chunk in token_chunks:
        cnt=cnt+1
        print(f'request is going to be made for chunk --- {chunk}')
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"Execute the following prompt as chunk nubmer {cnt} from bigger request split on total {len(token_chunks)} and prepare it so later all responses will be combined using += operation ### {prompt} " },
                {"role": "user", "content": chunk}
            ],
            temperature=temperature
        )
        summaries += (response.choices[0].message.content)

    # joined_summaries = ' '.join(summaries)
    # print(f'total number of received summaries is = {len(summaries)}')
    # print(f'joined summaries are going to be summarized ---- {joined_summaries}')
    # if len(summaries) > 1:
    #     final_summary_response = client.chat.completions.create(
    #         model=model,
    #         messages=[
    #             {"role": "system", "content": "Join the following summaries as a result from one big promt that could not be handled at once"},
    #             {"role": "user", "content": joined_summaries}
    #         ],
    #         temperature=temperature
    #     )
    #     final_summary = final_summary_response.choices[0].message.content
    # else:
    #     final_summary = summaries[0]

    return summaries


def prompt_with_chat_gpt(prompt, sysMessage, model="gpt-4", temperature=0.7):
    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": sysMessage},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content


def summarize_transcript(transcript):
    return summarize_long_text(transcript,
                                "Analyze the following meeting transcription and return short summarization", 8193)
