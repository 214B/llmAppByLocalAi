import os
import requests
from typing import List, Dict
import openai
import json

openai.api_key = "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"


def lookup_location_id(location: str):
    params = {
        "location": location,
        "key": 'a94f9c864ff54ab1bdb6c2657395789e'
    }
    response = requests.get(
        'https://geoapi.qweather.com/v2/city/lookup', params=params)
    # get the id of the first location
    location_id = response.json()['location'][0]['id']
    return location_id


def get_current_weather(location: str):
    location_id = lookup_location_id(location)
    params = {
        "location": location_id,
        "key": 'a94f9c864ff54ab1bdb6c2657395789e'
    }
    response = requests.get(
        'https://devapi.qweather.com/v7/weather/now', params=params)
    feelslike = response.json()['now']['feelsLike']
    text = response.json()['now']['text']
    humidity = response.json()['now']['humidity']
    return f"Temperature: {feelslike} Description: {text} Humidity: {humidity}"


def add_todo(todo: str):
    # Define the directory path and file path
    directory_path = 'store'
    file_path = os.path.join(directory_path, 'todos.txt')

    # Create the file if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        open(file_path, 'w+').close()

    # Open the file in append mode ('a+')
    with open(file_path, 'a+') as f:
        # Append the todo item to the file
        f.write('- ' + todo + '\n')
        # Move the file cursor to the beginning
        f.seek(0)
        # Read all todos from the file
        todos = f.read()

    # Return the todos
    return todos

def function_calling(messages: List[Dict], history):
    # fetch content
    content = messages[-1]['content']
    custom_funcs = [
        {
            'name': 'get_current_weather',
            'description': 'Get the current weather information for a given location.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'location': {
                        'type': 'string',
                        'description': 'The location for which to retrieve the weather information.'
                    }
                }
            }
        },
        {
            'name': 'add_todo',
            'description': 'Add a new todo item to a list of todos stored in a file.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'todo': {
                        'type': 'string',
                        'description': 'The todo item to add to the list.'
                    }
                }
            }
        }

    ]
    # openai function api
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': content}],
        functions=custom_funcs,
        function_call='auto'
    )

    data_json = dict(response)
    funcName = response["choices"][0]["message"]["function_call"]["name"]
    if funcName == 'get_current_weather':
        location = json.loads(response["choices"][0]["message"]["function_call"]["arguments"])["location"]
        response = get_current_weather(location)
        
        for r in response:
            yield r 
        
    elif funcName == 'add_todo':
        todo = json.loads(response["choices"][0]["message"]["function_call"]["arguments"])["todo"]
        add_todo_response = add_todo(todo)
        for r in add_todo_response:
            yield r

# 统一接口，包装原函数
def function_calling_wrapper(messages: List[Dict], history):
    yield function_calling(messages)

# 包测试代码
def function_calling_test(messages: List[Dict]):
    response = function_calling(messages, None)
    s = ""
    for res in response:
        s += res
    messages.append({"role": "assistant", "content": s})
    return messages

if __name__ == "__main__":
    messages = [
        {"role": "user", "content": "What's the weather like in Beijing?"}]
    print(function_calling_test(messages))

    messages = [{"role": "user", "content": "Add a todo: walk"}]
    print(function_calling_test(messages))
