import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import re
from bs4 import BeautifulSoup
import pytz

# env vars, headers, and timezone
load_dotenv()
owner = os.getenv('OWNER')
repo = os.getenv('REPO')
github_token = os.getenv('GITHUB_TOKEN')
headers = {
    'Authorization': f'token {github_token}'
}
local_tz = pytz.timezone('America/New_York')

def job():
    # get the current date
    local_time = datetime.now(local_tz).replace(hour=0, minute=0, second=0, microsecond=0)
    current_date = local_time.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

    parsed_internships = {}
    errors = 0
    commits = get_commits(start_date=current_date)    
    print(f"Found {len(commits)} commits")

    for commit in commits:
        try:
            sha = commit['sha']
            commit_data = get_commit(sha)
            parsed_internship = parse_commit(commit_data)
            company = parsed_internship['company']
            position = parsed_internship['position']
            intern_key = f"{company}:{position}"
            if intern_key not in parsed_internships:
                parsed_internships[intern_key] = parsed_internship
        except Exception as e:
            errors += 1 

    print(f"Found {len(parsed_internships)} internships. Removed {errors} due to errors.")
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

    # regex for splitting the diff string
    pattern = r'\n\+(.*?)\n'
    match = re.search(pattern, diff_string)
    
    if match:
        # Return the captured group (everything between '\n+' and '\n')
        raw = match.group(1)
    else:
        return None
    
    split_raw = raw.split('|')

    # company, position, location, url
    company = split_raw[1].strip()
    position = split_raw[2].strip()

    url_pattern = r'href="([^"]+)"'
    url_match = re.search(url_pattern, split_raw[4])
    url = url_match.group(1) if url_match else None

    location_html = split_raw[3]
    soup = BeautifulSoup(location_html, 'html.parser')
    locations = [loc.strip() for loc in soup.stripped_strings]

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