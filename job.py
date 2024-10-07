import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
owner = os.getenv('OWNER')
repo = os.getenv('REPO')
current_date = datetime.now().date().isoformat() + 'T00:00:00Z'

def job():
    parsed_internships = []
    commits = get_commits()    
    print(f"Found {len(commits)} commits")

    for commit in commits:
        try:
            sha = commit['sha']
            commit_data = get_commit(sha)
            print(commit_data)
            parsed_internship = parse_commit(commit_data)
            parsed_internships.append(parsed_internship)
        except Exception as e:
            print(f"Probably rate limited")

    return parsed_internships


def get_commits(start_date=current_date, end_date=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {}
    params['since'] = start_date
    params['until'] = end_date
    response = requests.get(url, params=params)
    return response.json()

def get_commit(sha: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
    response = requests.get(url)
    return response.json()

def parse_commit(commit):
    return [commit['files'][0]['patch'], commit['files'][0]['filename']]

if __name__ == "__main__":
    job()