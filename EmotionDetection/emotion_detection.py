import requests
import json

def emotion_detector(text_to_analyze):
    if not text_to_analyze or not text_to_analyze.strip():
        return {
            'anger': None, 'disgust': None, 'fear': None, 
            'joy': None, 'sadness': None, 'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}

    try:
        # Added a 10-second timeout to prevent infinite hanging
        response = requests.post(url, json=input_json, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return {
            'anger': None, 'disgust': None, 'fear': None, 
            'joy': None, 'sadness': None, 'dominant_emotion': None
        }

    if response.status_code == 400:
        return {
            'anger': None, 'disgust': None, 'fear': None, 
            'joy': None, 'sadness': None, 'dominant_emotion': None
        }

    response_dict = json.loads(response.text)
    emotions = response_dict['emotionPredictions'][0]['emotion']
    dominant_emotion = max(emotions, key=emotions.get)
    
    return {
        'anger': emotions.get('anger', 0),
        'disgust': emotions.get('disgust', 0),
        'fear': emotions.get('fear', 0),
        'joy': emotions.get('joy', 0),
        'sadness': emotions.get('sadness', 0),
        'dominant_emotion': dominant_emotion
    }