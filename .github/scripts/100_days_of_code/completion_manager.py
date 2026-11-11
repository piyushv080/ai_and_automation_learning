"""Complete an active challenge after owner review and solution-file check."""
import os
from github_api import add_comment, get, issue_day, remove_label, set_issue_labels

def main():
    number = int(os.environ["ISSUE_NUMBER"])
    body = os.environ.get("COMMENT_BODY", "").strip()
    actor = os.environ.get("COMMENT_USER", "")
    owner = os.environ["GITHUB_REPOSITORY_OWNER"]

    if body != "/complete":
        return
    if actor.casefold() != owner.casefold():
        print("Ignoring completion request from non-owner.")
        return

    issue = get(f"issues/{number}")
    if "pull_request" in issue or issue["state"] != "open":
        add_comment(number, "Completion rejected: issue is not open.")
        return

    labels = {x["name"] for x in issue.get("labels", [])}
    if "100-days-challenge" not in labels or "status-active" not in labels:
        add_comment(number, "Completion rejected: issue is not an active challenge.")
        return

    day = issue_day(issue)
    if day is None:
        raise RuntimeError("Challenge issue has no day-NNN label.")

    # Require a previous successful submission-check comment by github-actions[bot].
    comments = get(f"issues/{number}/comments?per_page=100")
    has_pass = any(
        c.get("user", {}).get("login") == "github-actions[bot]"
        and "Submission check: passed" in c.get("body", "")
        for c in comments
    )
    if not has_pass:
        add_comment(number, "Complete rejected: first comment `/submit` and pass the file check.")
        return

    remove_label(number, "status-active")
    remove_label(number, "stage-reasoning")
    current = {x["name"] for x in get(f"issues/{number}")["labels"]}
    current.add("status-completed")
    set_issue_labels(number, sorted(current))

    from github_api import patch
    patch(f"issues/{number}", {"state": "closed"})
    add_comment(number, f"Challenge Day {day:03d} marked completed. Congratulations!")
    print(f"Completed Day {day:03d}.")

if __name__ == "__main__":
    main()
