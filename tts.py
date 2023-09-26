
import requests
import os
import json
from typing import List, Dict
import uuid
import openai 

openai.api_key = "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"

def text2audio(content: str):
    print(content)
    url = 'http://localhost:8080/tts'
    # content = messages[-1]['content']
    payload = json.dumps({
        "input": content,
        "model": "en-us-blizzard_lessac-medium.onnx"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # Save the audio file
    id = uuid.uuid4()
    file_path = f'store/audio/{id}.mp3'

    # Ensure the directory path exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Create the empty file
    with open(file_path, 'w') as file:
        pass

    with open(file_path, 'wb') as f:
        f.write(response.content)
    
    # messages.append({"role": "assistant", "content": content})
    # history[-1][1] = (file_path, )
    # Return the audio file
    return file_path

def text2audio_wrapper(messages: List[Dict], history):
    
    respond = ""
    mess = []
    mess.append(messages[-1])
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = mess,
        stream = True   # 流式传输
    )

    # return completion
    for stream_response in completion:
        delta = dict(stream_response)['choices'][0]['delta']
        if 'content' in delta.keys():
            respond += delta['content']
        else:
            respond += ""
            
    file_path = text2audio(respond)
    messages.append({"role": "assistant", "content": respond})
    history[-1][1] = (file_path, )
    return messages, history
    

if __name__ == "__main__":
    print(text2audio("Sun Wukong (also known as the Great Sage of Qi Tian, Sun Xing Shi, and Dou Sheng Fu) is one of the main characters in the classical Chinese novel Journey to the West"))
