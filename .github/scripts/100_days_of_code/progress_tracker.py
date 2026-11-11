"""Print progress from official (non-test) challenge issues."""
from github_api import issue_day, list_challenge_issues

def main():
    issues = [
        issue for issue in list_challenge_issues()
        if "test-run" not in {x["name"] for x in issue.get("labels", [])}
    ]
    completed, active = set(), set()
    for issue in issues:
        day = issue_day(issue)
        if day is None:
            continue
        labels = {x["name"] for x in issue.get("labels", [])}
        if "status-completed" in labels:
            completed.add(day)
        elif issue["state"] == "open" and "status-active" in labels:
            active.add(day)

    print("=" * 45)
    print("100 DAYS OF CODE - OFFICIAL PROGRESS")
    print("=" * 45)
    print(f"Completed : {len(completed)} / 100")
    print(f"Active    : {len(active)}")
    print(f"Remaining : {100 - len(completed)}")
    print(f"Progress  : {len(completed):.0f}%")
    print("Completed days:", sorted(completed))
    print("Active days:", sorted(active))

if __name__ == "__main__":
    main()
