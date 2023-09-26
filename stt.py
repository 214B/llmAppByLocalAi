import subprocess

import requests
import json
import os

# curl http://localhost:8080/v1/audio/transcriptions -H "Content-Type: multipart/form-data" -F file="@D:\Desktop\kst.wav" -F model="whisper-1"


# PORT = '43.153.120.236:8080'
# PORT = '166.111.80.169:8080'

def messages2audio(messages):
    current_text = messages[-1]['content']
    text = audio2text(current_text)
    messages.append({'role': 'user', 'content': text})
    return messages


def audio2text(file):
    """
    TODO
    """
    print("file:", file)
    headers = {
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
    }

    files = {
        'file': open(file, 'rb'),
        'model': (None, 'whisper-1'),
    }

    current_text = ""
    # wav文件
    if file.endswith('.wav'):
        #
        response = requests.post('http://43.153.120.236:8080/v1/audio/transcriptions', headers=headers, files=files)
        print(response.json()['text'])
        current_text = response.json()['text']
    else:
        pass
    return current_text


if __name__ == "__main__":
    testPath = "D:\\Desktop\\kst.wav"
    audio2text(testPath)

