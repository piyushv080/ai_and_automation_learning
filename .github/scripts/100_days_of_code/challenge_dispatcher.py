
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CURRICULUM_FILE = ROOT / "curriculum" / "index.json"

API_URL = "https://api.github.com"

CHALLENGE_LABEL = "100-days-challenge"
ACTIVE_LABEL = "status-active"
COMPLETED_LABEL = "status-completed"
REASONING_LABEL = "stage-reasoning"


def load_curriculum():
    """Load and validate the challenge curriculum."""
    with CURRICULUM_FILE.open(encoding="utf-8") as file:
        curriculum = json.load(file)

    challenges = curriculum.get("challenges", [])

    if not challenges:
        raise ValueError("No challenges found in curriculum/index.json")

    for challenge in challenges:
        if not all(key in challenge for key in ("day", "title", "file")):
            raise ValueError(f"Invalid challenge entry: {challenge}")

        challenge_file = ROOT / challenge["file"]

        if not challenge_file.is_file():
            raise FileNotFoundError(
                f"Challenge file does not exist: {challenge_file}"
            )

    return sorted(challenges, key=lambda item: item["day"])


def github_request(endpoint, method="GET", payload=None):
    """Make an authenticated GitHub REST API request."""
    token = os.environ["GITHUB_TOKEN"]

    url = f"{API_URL}/repos/{os.environ['GITHUB_REPOSITORY']}/{endpoint}"

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else None
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8")
        raise RuntimeError(
            f"GitHub API error {error.code}: {details}"
        ) from error


def ensure_label(name, color, description):
    """Create a repository label if it does not already exist."""
    try:
        github_request(
            f"labels/{urllib.parse.quote(name, safe='')}"
        )
    except RuntimeError as error:
        if "404" not in str(error):
            raise

        github_request(
            "labels",
            method="POST",
            payload={
                "name": name,
                "color": color,
                "description": description,
            },
        )


def get_challenge_issues():
    """Get all issues belonging to this challenge."""
    issues = github_request(
        "issues?state=all&per_page=100"
        f"&labels={urllib.parse.quote(CHALLENGE_LABEL)}"
    )

    return [
        issue for issue in issues
        if "pull_request" not in issue
    ]


def issue_labels(issue):
    return {label["name"] for label in issue["labels"]}


def get_day_number(issue):
    """Extract day number from a day-NNN label."""
    for label in issue_labels(issue):
        if label.startswith("day-"):
            try:
                return int(label.split("-", 1)[1])
            except ValueError:
                continue
    return None


def main():
    repository = os.environ["GITHUB_REPOSITORY"]
    print(f"Repository: {repository}")

    challenges = load_curriculum()

    ensure_label(CHALLENGE_LABEL, "1D76DB", "100 Days of Code challenge")
    ensure_label(ACTIVE_LABEL, "FBCA04", "Currently active challenge")
    ensure_label(COMPLETED_LABEL, "0E8A16", "Challenge completed")
    ensure_label(REASONING_LABEL, "5319E7", "Reasoning stage")

    issues = get_challenge_issues()

    active_issues = [
        issue for issue in issues
        if issue["state"] == "open"
        and ACTIVE_LABEL in issue_labels(issue)
    ]

    if active_issues:
        print(f"Active challenge already exists: #{active_issues[0]['number']}")
        return

    completed_days = {
        get_day_number(issue)
        for issue in issues
        if COMPLETED_LABEL in issue_labels(issue)
    }

    next_challenge = next(
        (
            challenge for challenge in challenges
            if challenge["day"] not in completed_days
        ),
        None,
    )

    if next_challenge is None:
        print("All challenges have been completed!")
        return

    day = next_challenge["day"]
    day_label = f"day-{day:03d}"

    ensure_label(
        day_label,
        "C5DEF5",
        f"Day {day} challenge",
    )

    challenge_path = ROOT / next_challenge["file"]
    challenge_body = challenge_path.read_text(encoding="utf-8")

    body = (
        f"{challenge_body}\n\n"
        "---\n"
        "### How to submit\n"
        "Complete the challenge and comment `/submit` when ready.\n"
    )

    github_request(
        "issues",
        method="POST",
        payload={
            "title": f"Day {day:03d}: {next_challenge['title']}",
            "body": body,
            "labels": [
                CHALLENGE_LABEL,
                day_label,
                ACTIVE_LABEL,
                REASONING_LABEL,
            ],
        },
    )

    print(f"Created Day {day:03d}: {next_challenge['title']}")


if __name__ == "__main__":
    main()
