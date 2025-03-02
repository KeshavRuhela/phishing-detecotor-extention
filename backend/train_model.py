import pandas as pd
import numpy as np
import re
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Feature extraction function - must be identical to the one used in the API
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

# Load your CSV data
df = pd.read_csv('phishing_dataset.csv')

# Extract features from URLs
X = []
for url in df['url']:
    X.append(extract_features(url))

# Convert to numpy array
X = np.array(X)
y = df['label'].values

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, 'phishing_model.pkl')
print("Model saved as 'phishing_model.pkl'")