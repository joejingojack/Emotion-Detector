import requests
import json

def emotion_detector(text_to_analyze):
    """
    Detects emotions in the input text using the Watson Emotion API.

    Returns a dictionary with:
    - 'anger', 'disgust', 'fear', 'joy', 'sadness', 'dominant_emotion'
    If the server returns status_code 400 (bad request), or if the input is blank,
    all values are set to None.
    """

    # Handle blank input immediately
    if not text_to_analyze or text_to_analyze.strip() == "":
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    payload = { 
        "raw_document": { 
            "text": text_to_analyze 
        } 
    }
    
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        # Handle HTTP 400 (Bad Request)
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }

        response.raise_for_status()  # Raise exception for other non-200 responses

        data = response.json()

        # Extract emotions
        emotions = data['emotionPredictions'][0]['emotion']
        anger_score = emotions['anger']
        disgust_score = emotions['disgust']
        fear_score = emotions['fear']
        joy_score = emotions['joy']
        sadness_score = emotions['sadness']

        # Determine dominant emotion
        emotion_scores = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }

    except (requests.RequestException, KeyError, ValueError) as e:
        # Return all None if any unexpected error occurs
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }