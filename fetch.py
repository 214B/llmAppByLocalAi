import requests
from bs4 import BeautifulSoup
from chat import chat

def url2messages(messages, history):
    # print('msg: ', messages)
    url = messages[-1]['content']
    text = fetch(url)
    current_text = "Act as a summarizer. Please summarize {0}. The following is thecontent: \n\n{1}".format(url, text)
    # print(current_text)
    messages[-1]['content'] = current_text
    return (messages, history)

def _fetch(messages, history):
    messages, history = url2messages(messages, history)
    current_text = messages[-1]['content']
    messages.append({"role": "user", "content": current_text})
    generator = chat(messages, history)
    for stream_response in generator:
        yield stream_response

def fetch(url: str):
    """
    TODO
    """
    response = requests.get(url)
    html_content = response.text

    # 使用Beautiful Soup解析网页内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到目标<p>标签并提取文字信息
    target_p = soup.select_one("body > main > div > section > div.border-r10 > p:nth-child(3)")
    if target_p:
        text = target_p.get_text()
        # print(text)
    else:
        print("未找到目标<p>标签")
    return text


if __name__ == "__main__":
    fetch("https://dev.qweather.com/en/help")