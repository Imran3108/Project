from flask import Flask, render_template_string
import database

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerability Dashboard</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body { padding: 20px; }
        .High { color: red; font-weight: bold; }
        .Medium { color: orange; font-weight: bold; }
        .Safe { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-4">Vulnerability Detection Dashboard</h1>
        
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Total PRs Analyzed</h5>
                        <p class="card-text display-4">{{ total_prs }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Vulnerabilities Found</h5>
                        <p class="card-text display-4">{{ total_vulns }}</p>
                    </div>
                </div>
            </div>
        </div>

        <h3>Recent Detections</h3>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>PR #</th>
                    <th>File</th>
                    <th>Status</th>
                    <th>Severity</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                {% for row in results %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>{{ row[1] }}</td>
                    <td>{{ row[2] }}</td>
                    <td>{{ row[3] }}</td>
                    <td class="{{ row[4] }}">{{ row[4] }}</td>
                    <td>{{ row[5] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

@app.route('/dashboard')
def dashboard():
    results = database.get_all_results()
    
    total_prs = len(set(row[1] for row in results)) # Unique PR numbers
    total_vulns = sum(1 for row in results if row[3] == 'Vulnerable') # Check status column

    return render_template_string(HTML_TEMPLATE, results=results, total_prs=total_prs, total_vulns=total_vulns)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
