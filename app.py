import gradio as gr
import os
from function import function_calling
from image_generate import message2image
from stt import audio2text
from tts import text2audio_wrapper as text2audio
from search import _search
from pdf import generate_summary, read_txt, filechat
from mnist import imgclassification
import chat
from fetch import _fetch

messages = []
current_file_text = None

'''
聊天、语音输入不在下面列表中
'''
# 需要流式输出的函数
text_out_funcs = {
    '/search': _search,                         # 网络搜索
    '/fetch': _fetch,                           # 网页总结
    '/function': function_calling,              # 函数调用
    '/read_txt': read_txt,                      # 文件聊天_读取文件_自定义command
    '/file': filechat,                          # 文件聊天_回答问题
    '/imgclassification': imgclassification     # 图片分类
}
# 不需要流式输出的函数
no_text_funcs = {
    '/image': message2image,                    # 图片生成
    '/audio': text2audio,                       # 语音输出
}

def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.update(value="", interactive=False)

def add_file(history, file):
    history = history + [((file.name,), None)]
    return history

'''
流式输出的函数的统一接口
'''
def stream_func(func, messages, history):
    # 需要先置为字符串类型，否则for循环+=报错
    history[-1][1] = ""         
    
    generator = func(messages, history)   
    for stream_response in generator:
        history[-1][1] += stream_response
        yield history
       
    # 流式输出结束后更新messages
    messages.append({"role": "assistant", "content": history[-1][1]})  
    yield history


def bot(history):
    global messages
    current_text = history[-1][0]
    
    '''
    判断是否为文件路径
    (.wav)      by 李航
    (.txt .png) by 陈昊林
    如果为文件，预先处理
    '''
    if str(current_text[0]).endswith('.wav'):
        current_text = audio2text(str(current_text[0]))
    elif str(current_text[0]).endswith('.png'):
        current_text = '/imgclassification Please classify ' + current_text[0]
    elif str(current_text[0]).endswith('.txt'):
        history[-1][0] = current_text[0]
        with open(current_text[0],'r', encoding="utf-8") as f:
            prompt = f.read()
            current_text = generate_summary(prompt)
            current_text = '/read_txt ' + current_text

    # command
    if str(current_text).startswith('/'):
        # start_label为指令，如'/search'
        start_label = str(current_text).split(' ')[0]
        # current_text为指令后的内容，如' /search Sun Wukong' -> 'Sun Wukong'
        current_text = current_text[len(start_label):].strip()
        messages.append({"role": "user", "content": current_text})
        
        if(start_label in text_out_funcs.keys()):
            for stream_respose in stream_func(text_out_funcs[start_label], messages, history):
                yield stream_respose
        else:
            messages, history = no_text_funcs[start_label](messages, history)
        yield history
        
    # 正常聊天
    else:
        messages.append({"role": "user", "content": current_text})
        for stream_response in stream_func(chat.chat, messages, history):
            yield stream_response


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        clear_btn = gr.Button('Clear')
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio", "text"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )

    txt_msg.then(lambda:  gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear_btn.click(lambda: messages.clear(), None, chatbot, queue=False)

demo.queue()
demo.launch(share=True)
