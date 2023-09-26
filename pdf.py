import os
import re
import openai

openai.api_key = "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"

def generate_text(sumprompt):
    """
    TODO
    """
    messages = [{"role":"user", "content": sumprompt},{"role":"assistant", "content": "Hello"}]
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        stream = True   # 流式传输
    )
    for stream_response in completion:
        delta = dict(stream_response)['choices'][0]['delta']
        if 'content' in delta.keys():
            yield delta['content']
        else:
            yield ""



def generate_answer(current_file_text: str, content: str):
    """
    TODO
    """
    question = "阅读以下文段:\"" + current_file_text +  "\"回答下列问题:\"" + content + "\""
    return question

def generate_summary(current_file_text: str):
    """
    TODO
    """
    summary_prompt = "请总结以下文段:" + current_file_text
    return summary_prompt

def read_txt(messages, history):
    for stream_response in generate_text(messages[-1]['content']):
        yield stream_response

def filechat(messages, history):
    i = -1
    while 1:
        if history[i][0].endswith('.txt'):
            break
        i = i - 1
    with open(history[i][0], 'r', encoding='utf-8') as f:
        content = f.read()
        question = generate_answer(content, messages[-1]['content'])
        for stream_response in generate_text(question):
            yield stream_response

if __name__ == "__main__":
    prompt = generate_answer("Hello", "Who is Sun Wukong?")
    generate_text(prompt)