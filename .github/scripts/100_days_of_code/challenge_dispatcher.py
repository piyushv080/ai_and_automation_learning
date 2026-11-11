
"""
100 Days of Code - GitHub Issue Dispatcher

Creates one active GitHub Issue at a time from curriculum/index.json.
Uses GitHub's built-in GITHUB_TOKEN. No third-party dependencies.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[3]
CURRICULUM_FILE = ROOT / "curriculum" / "index.json"

API_URL = "https://api.github.com"

CHALLENGE_LABEL = "100-days-challenge"
ACTIVE_LABEL = "status-active"
COMPLETED_LABEL = "status-completed"
REASONING_LABEL = "stage-reasoning"

LABELS = {
    CHALLENGE_LABEL: ("1D76DB", "100 Days of Code challenge"),
    ACTIVE_LABEL: ("FBCA04", "Currently active challenge"),
    COMPLETED_LABEL: ("0E8A16", "Challenge completed"),
    REASONING_LABEL: ("5319E7", "Reasoning stage"),
}


# ---------------------------------------------------------
# GitHub API
# ---------------------------------------------------------

def github_request(endpoint, method="GET", payload=None):
    """Send an authenticated request to the GitHub REST API."""

    token = os.environ.get("GITHUB_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY")

    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable is missing.")

    if not repository:
        raise RuntimeError("GITHUB_REPOSITORY environment variable is missing.")

    url = f"{API_URL}/repos/{repository}/{endpoint}"

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
            f"GitHub API returned HTTP {error.code}: {details}"
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Could not connect to GitHub: {error}"
        ) from error


# ---------------------------------------------------------
# Curriculum
# ---------------------------------------------------------

def load_curriculum():
    """Load and validate all challenge definitions."""

    if not CURRICULUM_FILE.is_file():
        raise FileNotFoundError(
            f"Curriculum file not found: {CURRICULUM_FILE}"
        )

    with CURRICULUM_FILE.open(encoding="utf-8") as file:
        curriculum = json.load(file)

    challenges = curriculum.get("challenges", [])

    if not challenges:
        raise ValueError("No challenges found in curriculum.")

    seen_days = set()

    for challenge in challenges:
        required_fields = ("day", "title", "file")

        for field in required_fields:
            if field not in challenge:
                raise ValueError(
                    f"Challenge is missing '{field}': {challenge}"
                )

        day = challenge["day"]

        if not isinstance(day, int) or day < 1:
            raise ValueError(f"Invalid challenge day: {day}")

        if day in seen_days:
            raise ValueError(f"Duplicate challenge day: {day}")

        seen_days.add(day)

        challenge_path = (ROOT / challenge["file"]).resolve()

        if not challenge_path.is_relative_to(ROOT.resolve()):
            raise ValueError(
                f"Challenge file must be inside repository: {day}"
            )

        if not challenge_path.is_file():
            raise FileNotFoundError(
                f"Challenge file missing for Day {day}: {challenge_path}"
            )

    return sorted(challenges, key=lambda item: item["day"])


# ---------------------------------------------------------
# Labels
# ---------------------------------------------------------

def ensure_label(name, color, description):
    """Create a repository label if it does not already exist."""

    encoded_name = urllib.parse.quote(name, safe="")

    try:
        github_request(f"labels/{encoded_name}")
        print(f"Label exists: {name}")

    except RuntimeError as error:
        if "HTTP 404" not in str(error):
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

        print(f"Created label: {name}")


def ensure_all_labels():
    """Ensure every required label exists."""

    for name, (color, description) in LABELS.items():
        ensure_label(name, color, description)


# ---------------------------------------------------------
# Issue management
# ---------------------------------------------------------

def get_challenge_issues():
    """Retrieve all challenge issues, including closed issues."""

    issues = []
    page = 1

    while True:
        result = github_request(
            "issues?"
            f"state=all&per_page=100&page={page}"
            f"&labels={urllib.parse.quote(CHALLENGE_LABEL)}"
        )

        if not result:
            break

        # GitHub's Issues endpoint also returns pull requests.
        issues.extend(
            issue for issue in result
            if "pull_request" not in issue
        )

        if len(result) < 100:
            break

        page += 1

    return issues


def get_issue_labels(issue):
    return {label["name"] for label in issue.get("labels", [])}


def get_day_number(issue):
    """Read the day-NNN label from an issue."""

    for label in get_issue_labels(issue):
        if label.startswith("day-"):
            try:
                return int(label.split("-", 1)[1])
            except ValueError:
                continue

    return None


def update_issue_labels(issue_number, labels):
    """Replace an issue's labels with the supplied list."""

    github_request(
        f"issues/{issue_number}/labels",
        method="PUT",
        payload={"labels": sorted(labels)},
    )


def activate_issue(issue, challenge):
    """Reopen an unfinished issue and mark it active."""

    issue_number = issue["number"]
    day = challenge["day"]

    labels = get_issue_labels(issue)

    labels.discard(COMPLETED_LABEL)
    labels.add(CHALLENGE_LABEL)
    labels.add(ACTIVE_LABEL)
    labels.add(REASONING_LABEL)
    labels.add(f"day-{day:03d}")

    if issue["state"] == "closed":
        github_request(
            f"issues/{issue_number}",
            method="PATCH",
            payload={"state": "open"},
        )

        print(f"Reopened unfinished issue #{issue_number}")

    update_issue_labels(issue_number, labels)

    print(
        f"Day {day:03d} is active in existing issue #{issue_number}"
    )


def create_issue(challenge):
    """Create a real GitHub Issue for the next challenge."""

    day = challenge["day"]
    title = f"Day {day:03d}: {challenge['title']}"

    challenge_file = ROOT / challenge["file"]
    challenge_body = challenge_file.read_text(encoding="utf-8")

    topics = challenge.get("topics", [])
    difficulty = challenge.get("difficulty", "unspecified")

    body = (
        f"{challenge_body}\n\n"
        "---\n"
        "## Challenge tracking\n\n"
        f"- **Day:** {day}/100\n"
        f"- **Difficulty:** {difficulty}\n"
        f"- **Topics:** {', '.join(topics)}\n\n"
        "## Submission instructions\n\n"
        "Complete the challenge and submit your solution by "
        "commenting `/submit` on this issue.\n\n"
        "After reviewing your solution, mark this issue with "
        "`status-completed` to unlock the next challenge.\n"
    )

    labels = [
        CHALLENGE_LABEL,
        f"day-{day:03d}",
        ACTIVE_LABEL,
        REASONING_LABEL,
    ]

    issue = github_request(
        "issues",
        method="POST",
        payload={
            "title": title,
            "body": body,
            "labels": labels,
        },
    )

    print("=" * 60)
    print("CHALLENGE CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"Day: {day:03d}")
    print(f"Title: {title}")
    print(f"Issue number: #{issue['number']}")
    print(f"Issue URL: {issue['html_url']}")
    print("=" * 60)

    return issue


# ---------------------------------------------------------
# Main dispatcher
# ---------------------------------------------------------

def main():
    print("Starting 100 Days of Code dispatcher...")

    repository = os.environ.get("GITHUB_REPOSITORY")

    if not repository:
        raise RuntimeError("GITHUB_REPOSITORY is missing.")

    print(f"Repository: {repository}")

    # Validate curriculum before making GitHub changes.
    challenges = load_curriculum()

    print(f"Loaded {len(challenges)} challenges.")

    # Ensure all labels exist.
    ensure_all_labels()

    # Retrieve existing challenge issues.
    issues = get_challenge_issues()

    print(f"Existing challenge issues: {len(issues)}")

    completed_days = set()

    for issue in issues:
        if COMPLETED_LABEL in get_issue_labels(issue):
            day = get_day_number(issue)

            if day is not None:
                completed_days.add(day)

    print(f"Completed days: {sorted(completed_days)}")

    # Find the next challenge not yet completed.
    next_challenge = next(
        (
            challenge
            for challenge in challenges
            if challenge["day"] not in completed_days
        ),
        None,
    )

    if next_challenge is None:
        print("All available curriculum challenges are completed.")
        return

    next_day = next_challenge["day"]

    # Find an existing issue for the next incomplete challenge.
    existing_issue = next(
        (
            issue
            for issue in issues
            if get_day_number(issue) == next_day
        ),
        None,
    )

    if existing_issue:
        if existing_issue["state"] == "open":
            print(
                f"Challenge already exists and is open: "
                f"#{existing_issue['number']}"
            )
            return

        # Reopen an unfinished challenge rather than duplicating it.
        activate_issue(existing_issue, next_challenge)
        return

    # Create the next challenge issue.
    create_issue(next_challenge)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}")
        raise
