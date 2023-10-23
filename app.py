from flask import Flask, render_template, request
import requests
import os
import uuid
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from a .env file
load_dotenv()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    original_text = request.form['text']
    target_language = request.form['language']

    # Load API credentials and endpoint from environment variables
    subscription_key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + target_language
    constructed_url = endpoint + path + target_language_parameter

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': original_text}]

    translator_request = requests.post(constructed_url, headers=headers, json=body)
    translator_response = translator_request.json()

    translated_text = translator_response[0]['translations'][0]['text']

    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

if __name__ == '__main__':
    app.run(debug=True)
