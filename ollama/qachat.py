import requests

url = "http://localhost:11434/api/generate"

while True:
    prompt = input("You: ")

    if prompt.lower() in ["exit", "quit"]:
        break

    data = {
        "model": "qwen3-vl:2b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        print("Ollama:", result["response"])
    else:
        print("Error:", response.status_code, response.text)