
"""Generate a progress report from GitHub challenge issues."""

import json
import os
import urllib.request


API_URL = "https://api.github.com"


def get_issues():
    repository = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]

    issues = []
    page = 1

    while True:
        url = (
            f"{API_URL}/repos/{repository}/issues"
            f"?state=all&per_page=100&page={page}"
            "&labels=100-days-challenge"
        )

        request = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            batch = json.loads(response.read().decode("utf-8"))

        if not batch:
            break

        issues.extend(
            issue for issue in batch
            if "pull_request" not in issue
        )

        if len(batch) < 100:
            break

        page += 1

    return issues


def main():
    with open("curriculum/index.json", encoding="utf-8") as file:
        curriculum = json.load(file)

    total_days = curriculum["total_days"]
    issues = get_issues()

    completed = set()
    active = set()

    for issue in issues:
        day = None

        for label in issue.get("labels", []):
            name = label["name"]

            if name.startswith("day-"):
                try:
                    day = int(name.split("-", 1)[1])
                except ValueError:
                    pass

        if day is None:
            continue

        labels = {label["name"] for label in issue.get("labels", [])}

        if "status-completed" in labels:
            completed.add(day)
        elif "status-active" in labels and issue["state"] == "open":
            active.add(day)

    percentage = (len(completed) / total_days) * 100

    print("=" * 45)
    print("100 DAYS OF CODE - PROGRESS REPORT")
    print("=" * 45)
    print(f"Completed : {len(completed)} / {total_days}")
    print(f"Active    : {len(active)}")
    print(f"Remaining : {total_days - len(completed)}")
    print(f"Progress  : {percentage:.1f}%")
    print("=" * 45)

    print("Completed days:", sorted(completed))
    print("Active days:", sorted(active))


if __name__ == "__main__":
    main()
