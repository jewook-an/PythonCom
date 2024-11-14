import requests
import os 

API_KEY = os.getenv("perplexity_api_key")
url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "llama-3.1-sonar-small-128k-online",
    "messages": [
        {
            "role": "system",
            "content": "Be precise and concise."
        },
        {
            "role": "user",
            "content": "How many stars are there in our galaxy?"
        }
    ],
    "max_tokens": 512,
    "temperature": 0.2,
    "top_p": 0.9,
    "return_citations": True,
    "search_domain_filter": ["perplexity.ai"],
    "return_images": False,
    "return_related_questions": False,
    "search_recency_filter": "month",
    "top_k": 0,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 1
    }
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    }

response = requests.request("POST", url, json=payload, headers=headers)


# print(response.json()['choices'][0]['message']['content'] )


for cita in response.json()['citations']:
    print(cita)

# print(response.json()['citations'])