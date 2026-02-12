# backend/webhook.py

from fastapi import APIRouter, Request
import requests
import os
from dotenv import load_dotenv
import hybrid_detector
import database

load_dotenv()

router = APIRouter()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    print("\n--- PULL REQUEST RECEIVED ---")
    print("Event action:", payload.get("action"))

    # TEMPORARY: print even if action is not opened
    repo = payload.get("repository", {}).get("full_name")
    pr = payload.get("pull_request")

    if not repo or not pr:
        print("Not a pull request event")
        return {"message": "Not a PR event"}

    pr_number = pr.get("number")

    print(f"PR Opened: {repo} #{pr_number}")

    files = fetch_pr_files(repo, pr_number)

    # Database initialization (ensure tables exist)
    database.init_db()

    for file in files:
        filename = file.get("filename")
        patch = file.get("patch", "")
        
        print("\n----------------------------")
        print("File Name:", filename)
        
        # Perform Hybrid Analysis
        print("Analyzing code...")
        analysis_result = hybrid_detector.analyze(patch)
        
        # Log results
        status = "Vulnerable" if analysis_result["vulnerable"] else "Safe"
        severity = analysis_result["severity"]
        issues = analysis_result["issues"]
        
        print(f"Result: {status} ({severity})")
        for issue in issues:
            print(f"  - {issue}")
            
        # Save to Database
        database.save_result(pr_number, filename, status, severity)

    return {"message": "PR analyzed successfully"}


def fetch_pr_files(repo: str, pr_number: int):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    print("GitHub API Status:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        return []

    return response.json()
