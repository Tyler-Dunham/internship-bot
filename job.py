import requests
import os
from dotenv import load_dotenv
from utils import extract_data, get_time, regex_split_commit_changes

# env vars, headers, and timezone
load_dotenv()
owner = os.getenv('OWNER')
repo = os.getenv('REPO')
testing = os.getenv('TESTING', 'False').lower() in ('true', '1', 't')
github_token = os.getenv('GITHUB_TOKEN')
headers = {
    'Authorization': f'token {github_token}'
}

def job():
    # get the current date
    current_date = get_time(testing=testing)

    parsed_internships = {}
    errors = 0
    duplicates = 0

    commits = get_commits(start_date=current_date)    
    print(f"Found {len(commits)} commits")
    for commit in commits:
        try:
            sha = commit['sha']
            commit_data = get_commit(sha)
            parsed_internship = parse_commit(commit_data)
            company = parsed_internship['company']
            position = parsed_internship['position']
            internship_key = f"{company}:{position}"
            if internship_key not in parsed_internships:
                parsed_internships[internship_key] = parsed_internship
            else:
                duplicates += 1
        except Exception as e:
            errors += 1 

    print(f"Found {len(parsed_internships)} internships. Removed {duplicates} duplicate(s) and {errors} due to errors.")
    return parsed_internships

def get_commits(start_date=None, end_date=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {
        'since': start_date,
        'until': end_date
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def get_commit(sha: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
    response = requests.get(url, headers=headers)
    return response.json()

def parse_commit(commit):
    # readme of the commit
    diff_string = commit['files'][1]['patch'] if len(commit['files']) > 1 else commit['files'][0]['patch']
    split_raw = regex_split_commit_changes(diff_string)
    company, position, url, locations = extract_data(split_raw)

    # make parsed_internship object
    parsed_internship = {
        'company': company,
        'position': position,
        'location': locations,
        'url': url
    }

    return parsed_internship

if __name__ == "__main__":
    job()