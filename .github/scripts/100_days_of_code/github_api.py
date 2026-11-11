"""Small GitHub REST API helper using only the Python standard library."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"


def request(method, endpoint, payload=None):
    token = os.environ["GITHUB_TOKEN"]
    repository = os.environ["GITHUB_REPOSITORY"]
    url = f"{API}/repos/{repository}/{endpoint.lstrip('/')}"
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode()
            return json.loads(body) if body else None
    except urllib.error.HTTPError as exc:
        details = exc.read().decode(errors="replace")
        raise RuntimeError(f"GitHub API {exc.code}: {details}") from exc


def get(endpoint):
    return request("GET", endpoint)


def post(endpoint, payload):
    return request("POST", endpoint, payload)


def patch(endpoint, payload):
    return request("PATCH", endpoint, payload)


def put(endpoint, payload=None):
    return request("PUT", endpoint, payload)


def delete(endpoint):
    return request("DELETE", endpoint)


def list_challenge_issues():
    page = 1
    results = []
    while True:
        query = urllib.parse.urlencode({
            "state": "all", "per_page": 100, "page": page,
            "labels": "100-days-challenge",
        })
        batch = get(f"issues?{query}")
        batch = [x for x in batch if "pull_request" not in x]
        results.extend(batch)
        if len(batch) < 100:
            return results
        page += 1


def ensure_label(name, color, description):
    labels = get("labels?per_page=100")
    if any(item["name"].lower() == name.lower() for item in labels):
        return
    try:
        post("labels", {
            "name": name, "color": color, "description": description
        })
    except RuntimeError as exc:
        if "already_exists" not in str(exc):
            raise


def issue_day(issue):
    for label in issue.get("labels", []):
        name = label["name"]
        if name.startswith("day-"):
            try:
                return int(name[4:])
            except ValueError:
                return None
    return None


def add_comment(issue_number, body):
    return post(f"issues/{issue_number}/comments", {"body": body})


def set_issue_labels(issue_number, labels):
    return put(f"issues/{issue_number}/labels", {"labels": labels})


def remove_label(issue_number, label):
    try:
        delete(f"issues/{issue_number}/labels/{urllib.parse.quote(label, safe='')}")
    except RuntimeError as exc:
        if "404" not in str(exc):
            raise
