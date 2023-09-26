import os
import urllib.request

import openai
import os


def message2image(messages, history):
    current_text = messages[-1]['content']
    path = image_generate(current_text)
    messages.append({"role": "assistant", "content": current_text})
    history[-1][1] = (path, )
    # print(messages)
    return (messages, history)


def image_generate(content: str):
    """
    TODO
    """
    openai.api_key = "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"
    image_data = openai.Image.create(
        prompt=content,
        n=1,
        size="256x256"
    )
    image_url = dict(image_data['data'][0])['url']
    if not os.path.exists('image'):
        # 创建文件夹
        os.makedirs('image')
    else:
        print("文件夹已存在")
    file_path = 'image/picture.png'
    urllib.request.urlretrieve(image_url, file_path)
    return file_path


if __name__ == "__main__":
    image_generate('A cute baby sea otter')
