import static_analysis
import ml_model

def analyze(code_string):
    """
    Analyzes the code using both static analysis and ML model.
    Returns a structured dictionary with vulnerability status, severity, and details.
    """
    # 1. Run Static Analysis
    static_issues = static_analysis.scan(code_string)
    
    # 2. Run ML Prediction
    ml_result = ml_model.predict(code_string)
    ml_prediction = ml_result["prediction"]
    ml_confidence = ml_result["confidence"]

    # 3. Combine Results
    is_vulnerable = False
    severity = "Safe"
    issues = list(static_issues)

    if ml_prediction == 1:
        issues.append(f"ML Model detected vulnerability with confidence: {ml_confidence:.2f}")

    if len(static_issues) > 0 and ml_prediction == 1:
        is_vulnerable = True
        severity = "High"
    elif len(static_issues) > 0 or ml_prediction == 1:
        is_vulnerable = True
        severity = "Medium"
    
    return {
        "vulnerable": is_vulnerable,
        "severity": severity,
        "issues": issues
    }

if __name__ == "__main__":
    # Test
    code = "eval(user_input)"
    result = analyze(code)
    print("Analysis Result:")
    print(result)
