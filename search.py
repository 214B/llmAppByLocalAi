import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from chat import chat

def _search(messages, history):
    content = messages[-1]["content"]
    search_results = search(content)
    messages.append({"role": "assistant", "content": search_results})
    messages.append({"role": "user", "content": f"Please answer {content} based on the searchresult: \n\n{search_results}"})
    
    generator = chat(messages, history)
    for stream_response in generator:
        yield stream_response
        
def search(content: str):
    params = {
        "engine": "bing",
        "q": content,
        "api_key": "534868baf09daec6ec3ef44589bbcb550e4bbfa24d4a5a93a924d3b12c2716cf"
    }
    search = GoogleSearch(params)
    result = search.get_dict()
    origin_results = result['organic_results']
    for i in range(len(origin_results)):
        if "snippet" in origin_results[i].keys():
            search_results = origin_results[i]["snippet"]
            return search_results
    print("No search results found.")
    return "No search results found."

if __name__ == "__main__":
    print(search("Sun Wukong"))