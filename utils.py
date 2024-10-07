import re
from bs4 import BeautifulSoup
import pytz
from datetime import datetime

def get_time(testing: bool = False):
    if testing:
        date = datetime(2024, 10, 6).isoformat() + 'Z'
        return date
    
    local_tz = pytz.timezone('America/New_York')
    local_time = datetime.now(local_tz).replace(hour=0, minute=0, second=0, microsecond=0)
    current_date = local_time.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
    return current_date

def get_cron_times(testing: bool = False):
    if testing:
        # get actual hour and minute
        local_tz = pytz.timezone('America/New_York')
        local_time = datetime.now(local_tz)
        return {
            'hour': local_time.hour,
            'minute': local_time.minute + 1
        }
    
    return {
        'hour': 23,
        'minute': 59
    }

def regex_split_commit_changes(string: str):
    pattern = r'\n\+(.*?)\n'
    match = re.search(pattern, string)
    if match:
        raw = match.group(1)
    else:
        return None
    return raw.split('|')

def extract_data(data: list):
    company = data[1].strip()
    position = data[2].strip()

    url_pattern = r'href="([^"]+)"'
    url_match = re.search(url_pattern, data[4])
    url = url_match.group(1) if url_match else None

    location_html = data[3]
    soup = BeautifulSoup(location_html, 'html.parser')
    locations = [loc.strip() for loc in soup.stripped_strings]

    return company, position, url, locations