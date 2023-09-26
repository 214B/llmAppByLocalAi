import os
import openai

openai.api_key = "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"

def chat(messages, history):

    """
    TODO
    """
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        stream = True   # 流式传输
    )

    # return completion
    for stream_response in completion:
        delta = dict(stream_response)['choices'][0]['delta']
        if 'content' in delta.keys():
            yield delta['content']
        else:
            yield ""