import requests

API_KEY = 'sk-D4jDKCo13ceoaV0l2UcGcFGQdao2OoVfClnUsSf5kDj0GjOZ'

# This function is called from txtiapp/views.py
def generate_image(text):
    url = 'https://api.stability.ai/v1/text2img/generate'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'text': text,
        'output_format': 'png',
    }
    # This is the request to the API
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.content
    else:
        return None
