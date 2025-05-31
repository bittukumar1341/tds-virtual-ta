import requests

NGROK_URL = "https://5db1-49-37-72-98.ngrok-free.app"  # Replace this with your ngrok URL

def test_api(question):
    payload = {"question": question}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(NGROK_URL + "/", json=payload, headers=headers)
    if response.ok:
        data = response.json()
        print(f"Question: {question}")
        print(f"Answer: {data.get('answer')}")
        print(f"Links: {data.get('links')}")
    else:
        print("Request failed:", response.status_code, response.text)

if __name__ == "__main__":
    test_api("Should I use gpt-4o-mini or gpt3.5 turbo?")
