import re

def scan(code_string):
    """
    Scans the given code string for common vulnerabilities using regex.
    Returns a list of detected issues.
    """
    issues = []
    
    # Check for SQL Injection (simulated)
    # Looks for string concatenation in SQL queries
    sql_pattern = re.compile(r'(SELECT|INSERT|UPDATE|DELETE).*"\s*\+\s*\w+', re.IGNORECASE)
    if sql_pattern.search(code_string):
        issues.append("Potential SQL Injection detected (unsafe string concatenation).")

    # Check for Hardcoded Passwords
    # Looks for variable names like 'password', 'secret', etc. assigned to string literals
    password_pattern = re.compile(r'(password|secret|key)\s*=\s*["\'].+["\']', re.IGNORECASE)
    if password_pattern.search(code_string):
        issues.append("Hardcoded secret or password detected.")

    # Check for Unsafe eval()
    # Looks for usage of eval() function
    eval_pattern = re.compile(r'\beval\s*\(', re.IGNORECASE)
    if eval_pattern.search(code_string):
        issues.append("Unsafe usage of 'eval()' detected.")

    return issues

if __name__ == "__main__":
    # Test cases
    test_code = """
    user_input = "admin"
    query = "SELECT * FROM users WHERE name = " + user_input
    password = "supersecretpassword"
    eval("print('hello')")
    """
    print("Scanning test code...")
    detected = scan(test_code)
    for issue in detected:
        print(f"- {issue}")
