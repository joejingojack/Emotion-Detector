import unittest
from unittest.mock import patch, MagicMock
import json
from EmotionDetection.emotion_detection import emotion_detector

class TestEmotionDetector(unittest.TestCase):

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_statements(self, mock_post):
        test_cases = [
            ("I am glad this happened", "joy"),
            ("I am really mad about this", "anger"),
            ("I feel disgusted just hearing about this", "disgust"),
            ("I am so sad about this", "sadness"),
            ("I am really afraid that this will happen", "fear")
        ]

        emotion_responses = {
            "joy":    {"anger":0.1, "disgust":0.1, "fear":0.1, "joy":0.9, "sadness":0.0},
            "anger":  {"anger":0.9, "disgust":0.1, "fear":0.1, "joy":0.0, "sadness":0.0},
            "disgust":{"anger":0.1, "disgust":0.9, "fear":0.1, "joy":0.0, "sadness":0.0},
            "sadness":{"anger":0.0, "disgust":0.1, "fear":0.1, "joy":0.1, "sadness":0.9},
            "fear":   {"anger":0.1, "disgust":0.1, "fear":0.9, "joy":0.0, "sadness":0.0}
        }

        for text, expected_dominant in test_cases:
            mock_response = MagicMock()
            mock_response.text = json.dumps({
                "emotionPredictions": [
                    {"emotion": emotion_responses[expected_dominant]}
                ]
            })
            mock_post.return_value = mock_response

            result = emotion_detector(text)
            self.assertEqual(result['dominant_emotion'], expected_dominant)

            for key in ["anger", "disgust", "fear", "joy", "sadness"]:
                self.assertIn(key, result)

if __name__ == '__main__':
    unittest.main()
