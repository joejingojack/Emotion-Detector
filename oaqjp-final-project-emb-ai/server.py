'''
Executing this function initiates the application of emotion
analysis to be executed over the Flask channel and deployed on
localhost:5000.
'''

import sys
import os

# ADD PARENT DIRECTORY TO PYTHON PATH
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PARENT_DIR)

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

# Initialize Flask app
app = Flask(__name__)


@app.route("/emotionDetector")
def emo_detector():
    '''
    This function receives the text dynamically from the user
    and returns the formatted emotion analysis response.
    '''

    text_to_analyze = request.args.get("textToAnalyze")

    if not text_to_analyze or text_to_analyze.strip() == "":
        return "Invalid input! Please enter a valid statement."

    try:
        response = emotion_detector(text_to_analyze)

        # Dynamically extract everything (NO defaults)
        anger = response["anger"]
        disgust = response["disgust"]
        fear = response["fear"]
        joy = response["joy"]
        sadness = response["sadness"]
        dominant_emotion = response["dominant_emotion"]

        # Fully dynamic, never hardcoded
        return (
            f"For the given statement, the system response is "
            f"'anger': {anger}, "
            f"'disgust': {disgust}, "
            f"'fear': {fear}, "
            f"'joy': {joy} and "
            f"'sadness': {sadness}. "
            f"The dominant emotion is {dominant_emotion}."
        )

    except Exception as e:
        return f"Error occurred while processing the request: {str(e)}"


@app.route("/")
def render_index_page():
    '''
    This function renders the main application page.
    '''
    return render_template("index.html")


if __name__ == "__main__":
    '''
    This function executes the flask app and 
    deploys it on localhost:5000.
    '''
    app.run(host="0.0.0.0", port=5000, debug=True)