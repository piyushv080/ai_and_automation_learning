
"""
100 Days of Code - Submission Validator

Checks a /submit request against the active GitHub challenge.
It checks repository files but never executes submitted code.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request


API_URL = "https://api.github.com"


def github_request(endpoint):
    token = os.environ["GITHUB_TOKEN"]
    repository = os.environ["GITHUB_REPOSITORY"]

    request = urllib.request.Request(
        f"{API_URL}/repos/{repository}/{endpoint}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        details = error.read().decode("utf-8")
        raise RuntimeError(
            f"GitHub API error {error.code}: {details}"
        ) from error


def post_issue_comment(issue_number, message):
    token = os.environ["GITHUB_TOKEN"]
    repository = os.environ["GITHUB_REPOSITORY"]

    payload = json.dumps({"body": message}).encode("utf-8")

    request = urllib.request.Request(
        f"{API_URL}/repos/{repository}/issues/{issue_number}/comments",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def get_day_number(issue):
    for label in issue.get("labels", []):
        name = label["name"]
        if name.startswith("day-"):
            try:
                return int(name.split("-", 1)[1])
            except ValueError:
                pass
    return None


def check_solution(day):
    """Check for at least one Python file in the expected solution folder."""

    branch = os.environ.get(
        "SOLUTION_BRANCH",
        os.environ.get("GITHUB_DEFAULT_BRANCH", "main"),
    )

    folder = f"solutions/day-{day:03d}"
    encoded_path = urllib.parse.quote(folder, safe="/")
    encoded_branch = urllib.parse.quote(branch, safe="")

    contents = github_request(
        f"contents/{encoded_path}?ref={encoded_branch}"
    )

    if not isinstance(contents, list):
        return False, (
            f"No solution directory found at `{folder}/` "
            f"on branch `{branch}`."
        )

    python_files = [
        item["name"]
        for item in contents
        if item.get("type") == "file"
        and item.get("name", "").endswith(".py")
    ]

    if not python_files:
        return False, (
            f"No Python solution file found in `{folder}/` "
            f"on branch `{branch}`."
        )

    return True, python_files


def main():
    issue_number = os.environ["ISSUE_NUMBER"]
    comment_body = os.environ.get("COMMENT_BODY", "").strip()
    comment_user = os.environ.get("COMMENT_USER", "").strip()
    repository_owner = os.environ["GITHUB_REPOSITORY_OWNER"].strip()

    if comment_body != "/submit":
        print("Comment is not an exact /submit command. Nothing to do.")
        return

    if comment_user.casefold() != repository_owner.casefold():
        print("Submission ignored: commenter is not the repository owner.")
        return

    issue = github_request(f"issues/{issue_number}")

    if not issue:
        raise RuntimeError(f"Issue #{issue_number} was not found.")

    if "pull_request" in issue:
        raise RuntimeError("Pull request comments are not challenge submissions.")

    if issue["state"] != "open":
        post_issue_comment(
            issue_number,
            "Submission not accepted: this challenge issue is not open.",
        )
        return

    labels = {label["name"] for label in issue.get("labels", [])}

    if "100-days-challenge" not in labels:
        raise RuntimeError("This issue is not a 100 Days of Code challenge.")

    if "status-active" not in labels:
        post_issue_comment(
            issue_number,
            "Submission not accepted: this challenge is not marked active.",
        )
        return

    day = get_day_number(issue)

    if day is None:
        raise RuntimeError("No valid day-NNN label was found on this issue.")

    valid, result = check_solution(day)

    if not valid:
        post_issue_comment(
            issue_number,
            "## Submission check: not ready\n\n"
            f"{result}\n\n"
            "Push your Python solution to the configured branch, "
            "then comment `/submit` again.",
        )
        return

    files = "\n".join(f"- `{name}`" for name in result)

    post_issue_comment(
        issue_number,
        "## Submission check: passed\n\n"
        f"Found a Python solution for **Day {day:03d}**:\n\n"
        f"{files}\n\n"
        "This is a file-presence check only. Your code has not been "
        "executed or graded. Please review your solution and apply "
        "`status-completed` when you are satisfied.",
    )

    print(f"Submission file check passed for Day {day:03d}.")


if __name__ == "__main__":
    main()
