"""Validate /submit requests by checking for a committed Python solution file."""
import os
import sys
from github_api import add_comment, get, issue_day

def main():
    number = int(os.environ["ISSUE_NUMBER"])
    body = os.environ.get("COMMENT_BODY", "").strip()
    actor = os.environ.get("COMMENT_USER", "")
    owner = os.environ["GITHUB_REPOSITORY_OWNER"]

    if body != "/submit":
        return
    if actor.casefold() != owner.casefold():
        print("Ignoring submission from non-owner.")
        return

    issue = get(f"issues/{number}")
    if "pull_request" in issue or issue["state"] != "open":
        print("Issue is not an open challenge.")
        return

    labels = {x["name"] for x in issue.get("labels", [])}
    if "100-days-challenge" not in labels or "status-active" not in labels:
        add_comment(number, "Submission rejected: this is not an active challenge issue.")
        return

    day = issue_day(issue)
    if day is None:
        add_comment(number, "Submission rejected: missing day-NNN label.")
        return

    branch = os.environ.get("SOLUTION_BRANCH", "feature/100-days-of-code")
    folder = f"solutions/day-{day:03d}"
    try:
        contents = get(f"contents/{folder}?ref={branch}")
    except RuntimeError as exc:
        if "404" in str(exc):
            contents = []
        else:
            raise

    files = [
        item["name"] for item in (contents or [])
        if item.get("type") == "file" and item.get("name", "").endswith(".py")
    ]
    if not files:
        add_comment(
            number,
            f"## Submission check: not ready\n\n"
            f"No Python file found in `{folder}/` on branch `{branch}`.\n\n"
            "Push your solution and comment `/submit` again.",
        )
        return

    add_comment(
        number,
        "## Submission check: passed\n\n"
        + "\n".join(f"- `{folder}/{name}`" for name in files)
        + "\n\nThis checks file presence only; it does not execute or grade code. "
          "Review your solution and tests, then comment `/complete` when ready.",
    )
    print(f"Submission file check passed for day {day:03d}.")

if __name__ == "__main__":
    main()
