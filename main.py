import requests
from requests.auth import HTTPBasicAuth
import json
import os
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Replace with your actual values
token = os.getenv("token")
default_space_id = os.getenv("default_space_id")

# Read your Markdown file
markdown_file_path = Path("./test.md")
markdown_file_content = markdown_file_path.read_text(encoding="utf-8")

# Parse front matter using gray-matter equivalent
front_matter = {
    k.lower(): v
    for k, v in (
        line.split(":", 1)
        for line in matter(markdown_file_content).frontmatter.split("\n")
        if line
    )
}


# Get spaceId from spaceKey using an example function
def get_space_id_from_space_key(space_key):
    # Add your logic to get spaceId from spaceKey
    # For example, make a request to the space API endpoint
    return "<space_id>"


space_id = (
    front_matter.get("spaceid")
    or get_space_id_from_space_key(front_matter.get("spacekey"))
    or default_space_id
)

# Construct the request payload
body_data = {
    "spaceId": space_id,
    "status": front_matter.get("status", "current"),
    "title": front_matter.get("title", "title"),
    "parentId": front_matter.get("parentid"),
    "body": {
        "representation": "storage",
        "value": matter(
            markdown_file_content
        ).content,  # Use the content without front matter
    },
}

url = "https://edraaktechnologies.atlassian.net/wiki/api/v2/pages"
auth = HTTPBasicAuth("abdelmounim.b@edraak.io", token)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# Make the API request
response = requests.post(url, data=json.dumps(body_data), headers=headers, auth=auth)

print(json.dumps(response.json(), sort_keys=True, indent=4, separators=(",", ": ")))
