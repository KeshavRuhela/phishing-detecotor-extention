import re
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained phishing detection model
model = joblib.load('phishing_model.pkl')


@app.route('/')
def home():
    return "Flask API is running! Use the /check_url endpoint."


@app.route('/check_url', methods=['POST'])
def check_url():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'Missing "url" field in request'}), 400

        url = data['url']

        # Extract features from the URL
        features = extract_features(url)

        # Reshape features for prediction
        features_array = np.array(features).reshape(1, -1)

        # Make a prediction
        prediction = model.predict(features_array)

        # Add more detailed response
        result = {
            'url': url,
            'phishing': bool(prediction[0]),
            'features': {
                'url_length': features[0],
                'dot_count': features[1],
                'at_sign_count': features[2],
                'hyphen_count': features[3],
                'underscore_count': features[4],
                'question_mark_count': features[5],
                'equals_sign_count': features[6],
                'slash_count': features[7],
                'phishing_keyword_count': features[8],
                'has_https': bool(features[9]),
                'has_ip_address': bool(features[10]),
                'is_shortened_url': bool(features[11]),
                'subdomain_count': features[12]
            }
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def extract_features(url):
    """
    Feature extraction function.
    """
    features = []

    # 1️⃣ URL Length
    features.append(len(url))

    # 2️⃣ Count Special Characters
    features.append(url.count('.'))
    features.append(url.count('@'))
    features.append(url.count('-'))
    features.append(url.count('_'))
    features.append(url.count('?'))
    features.append(url.count('='))
    features.append(url.count('/'))

    # 3️⃣ Presence of Phishing Keywords
    phishing_keywords = ['verify', 'bank', 'secure', 'update', 'account', 'login', 'confirm', 'password', 'paypal']
    features.append(sum(1 for word in phishing_keywords if word in url.lower()))

    # 4️⃣ Check for HTTPS
    features.append(1 if url.startswith('https') else 0)

    # 5️⃣ Check for IP Address in URL
    features.append(1 if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0)

    # 6️⃣ Check for Shortened URL (e.g., bit.ly, tinyurl)
    shortened_domains = ['bit.ly', 'goo.gl', 'tinyurl', 'ow.ly']
    features.append(1 if any(domain in url for domain in shortened_domains) else 0)

    # 7️⃣ Check for Subdomains
    features.append(url.count('.') - 1 if url.count('.') > 1 else 0)

    return features


if __name__ == '__main__':
    app.run(debug=True)