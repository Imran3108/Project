import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

MODEL_FILE = "vuln_model.pkl"
VECTORIZER_FILE = "tfidf_vectorizer.pkl"
DATASET_FILE = "dataset.csv"

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

def train_model():
    """
    Trains multiple models, selects the best one, and generates a comparison plot.
    Models compared: Logistic Regression, Random Forest, SVM.
    """

    if not os.path.exists(DATASET_FILE):
        print(f"Error: {DATASET_FILE} not found.")
        return

    df = pd.read_csv(DATASET_FILE)
    
    # Preprocessing
    X = df['code']
    y = df['label']

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    X_tfidf = vectorizer.fit_transform(X)

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

    # Define Models
    models = {
        "Logistic Regression": LogisticRegression(),
        "Random Forest": RandomForestClassifier(n_estimators=100),
        "SVM": SVC(probability=True)
    }

    best_model = None
    best_accuracy = 0
    best_name = ""
    accuracies = {}

    print("\n--- ML Model Comparison ---")
    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        accuracies[name] = accuracy
        print(f"{name} Accuracy: {accuracy * 100:.2f}%")
        
        if accuracy >= best_accuracy:
            best_accuracy = accuracy
            best_model = model
            best_name = name

    print(f"\nBest Model Selected: {best_name} with {best_accuracy * 100:.2f}% accuracy.")
    
    # Generate Comparison Plot
    plt.figure(figsize=(10, 6))
    plt.bar(list(models.keys()), [score * 100 for score in accuracies.values()], color=['blue', 'green', 'red'])
    plt.xlabel('ML Models')
    plt.ylabel('Accuracy (%)')
    plt.title('Vulnerability Detection Model Accuracy Comparison')
    plt.ylim(0, 100)
    for i, v in enumerate(accuracies.values()):
        plt.text(i, v * 100 + 1, f"{v*100:.1f}%", ha='center')
    
    plt.savefig('model_comparison.png')
    print("Comparison chart saved as 'model_comparison.png'")
    
    # Retrain best model on full dataset
    best_model.fit(X_tfidf, y)

    # Save Model and Vectorizer
    joblib.dump(best_model, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)
    print("Best model and vectorizer saved successfully.\n")

def predict(code_string):
    """
    Predicts if the code_string is vulnerable.
    Returns a dictionary with prediction (0 or 1) and confidence score.
    """
    if not os.path.exists(MODEL_FILE) or not os.path.exists(VECTORIZER_FILE):
        print("Model files not found. Training new model...")
        train_model()

    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)

    code_tfidf = vectorizer.transform([code_string])
    prediction = model.predict(code_tfidf)[0]
    probabilities = model.predict_proba(code_tfidf)[0]
    
    # Confidence is the probability of the predicted class
    confidence = probabilities[prediction]

    return {
        "prediction": int(prediction),
        "confidence": float(confidence)
    }

if __name__ == "__main__":
    train_model()
    
    # Test
    test_code = "eval(user_input)"
    result = predict(test_code)
    print(f"Test Code: {test_code}")
    print(f"Result: {result}")
