import requests

def job():
    parsed_internships = []
    commits = get_commits()
    for commit in commits:
        commit_data = get_commit(commit['sha'])
        parsed_commit = parse_commit(commit_data)
        parsed_internships.append(parsed_commit)

    return parsed_internships


def get_commits():
    url = "https://api.github.com/repos/username/repo/commits"
    response = requests.get(url)
    return response.json()

def get_commit(sha: str):
    url = f"https://api.github.com/repos/username/repo/commits/{sha}"
    response = requests.get(url)
    return response.json()

def parse_commit(commit):
    return {}