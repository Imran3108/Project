from hybrid_detector import analyze
from database import save_result, init_db

def simulate_webhook_event(pr_number, filename, code_content):
    print(f"\nProcessing PR #{pr_number} - File: {filename}")
    
    # 1. Analyze Code
    result = analyze(code_content)
    
    print("Analysis Result:", result)
    
    # 2. Save to Database
    status = "Vulnerable" if result["vulnerable"] else "Safe"
    severity = result["severity"]
    
    save_result(pr_number, filename, status, severity)
    print("--------------------------------------------------")

if __name__ == "__main__":
    # Ensure DB is initialized
    init_db()

    # Test Cases
    test_cases = [
        (101, "login.py", "user_input = request.args.get('user')\nquery = 'SELECT * FROM users WHERE name = ' + user_input"),
        (102, "config.py", "password = 'supersecret123'\nprint('Config loaded')"),
        (103, "utils.py", "def greet(name):\n    print(f'Hello {name}')"),
        (104, "admin.py", "import os\nos.system('rm -rf /')"),
        (105, "unsafe.py", "eval('print(5 + 5)')")
    ]

    print("Simulating Webhook Events...")
    for pr, fname, code in test_cases:
        simulate_webhook_event(pr, fname, code)
    
    print("\nSimulation Complete. Check 'vulnerability_results.db' or run 'dashboard.py'.")
