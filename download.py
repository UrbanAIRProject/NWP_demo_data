import os
import requests
from bs4 import BeautifulSoup

from versions import UrbanAirData

# Target URL
#base_url = "http://exporter.nsc.liu.se/8a930c993fe54eedbdd7d4451b45ea57"
version = UrbanAirData.current_version
base_url = UrbanAirData.base_url
output_dir = "data"

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Start session
print(f"Download UrbanAir data v{version} from {base_url}")
session = requests.Session()
response = session.get(base_url)

# Check for success
if response.status_code != 200:
    print(f"Failed to access {base_url}: Status code {response.status_code}")
    exit(1)

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find all download links
links = soup.find_all('a', href=True)

downloaded = 0
# Filter 
hrefs = [link['href'] for link in links if not any([x in link['href'] for x in ['/', '?']])]

print(f"Expect {len(hrefs)} files")

for href in hrefs:
    file_url = os.path.join(base_url, href)
    file_name = os.path.basename(href)
    file_path = os.path.join(output_dir, file_name)
    if os.path.isfile(file_path):
       print(f"{file_url} already exists as {file_path}")
    else:
       print(f"Downloading {file_url} to {file_path}")
       file_resp = session.get(file_url)
       if file_resp.status_code == 200:
           with open(file_path, 'wb') as f:
               f.write(file_resp.content)
           downloaded += 1
       else:
           print(f"Failed to download {file_url}: Status code {file_resp.status_code}")

print(f"Downloaded {downloaded} files to '{output_dir}'")

