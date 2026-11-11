"""Create the next eligible daily challenge issue."""
import argparse
import json
import os
from datetime import date, datetime, timezone
from pathlib import Path

from github_api import (
    add_comment, ensure_label, issue_day, list_challenge_issues, post,
)

ROOT = Path(__file__).resolve().parents[3]
CURRICULUM = ROOT / "curriculum" / "index.json"


def load_curriculum():
    data = json.loads(CURRICULUM.read_text(encoding="utf-8"))
    if data.get("total_days") != 100:
        raise ValueError("Curriculum total_days must be 100.")
    days = [item["day"] for item in data["challenges"]]
    if len(days) != len(set(days)):
        raise ValueError("Duplicate challenge day found.")
    for item in data["challenges"]:
        if not (ROOT / item["file"]).is_file():
            raise FileNotFoundError(item["file"])
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-test", action="store_true")
    args = parser.parse_args()

    curriculum = load_curriculum()
    start = date.fromisoformat(curriculum["start_date"])
    today = datetime.now(timezone.utc).date()
    if not args.force_test and today < start:
        print(f"Official challenge starts {start}; no issue created.")
        return

    issues = list_challenge_issues()
    production_issues = [
        issue for issue in issues
        if "test-run" not in {x["name"] for x in issue.get("labels", [])}
    ]

    active = [
        issue for issue in production_issues
        if issue["state"] == "open"
        and "status-active" in {x["name"] for x in issue.get("labels", [])}
    ]
    if active and not args.force_test:
        print(f"An active challenge already exists: #{active[0]['number']}")
        return

    completed = {
        issue_day(issue)
        for issue in production_issues
        if "status-completed" in {x["name"] for x in issue.get("labels", [])}
    }
    completed.discard(None)

    if args.force_test:
        day = 1
    else:
        elapsed_day = (today - start).days + 1
        if elapsed_day < 1 or elapsed_day > 100:
            print("Outside the 100-day challenge window.")
            return
        day = max(completed, default=0) + 1
        if day > elapsed_day:
            print(
                f"Day {day:03d} is not scheduled yet. "
                f"Calendar day is {elapsed_day:03d}."
            )
            return

    challenge = next(
        (item for item in curriculum["challenges"] if item["day"] == day),
        None,
    )
    if challenge is None:
        print(f"No curriculum entry for day {day}.")
        return

    existing = [
        issue for issue in issues
        if issue_day(issue) == day
        and ("test-run" in {x["name"] for x in issue.get("labels", [])})
        == args.force_test
    ]
    if existing:
        print(f"Day {day:03d} issue already exists: #{existing[0]['number']}")
        return

    labels = [
        ("100-days-challenge", "1D76DB", "100 Days of Code challenge"),
        (f"day-{day:03d}", "C5DEF5", f"Challenge day {day:03d}"),
        ("status-active", "0E8A16", "Challenge currently active"),
        ("stage-reasoning", "5319E7", "Challenge is in progress"),
    ]
    if args.force_test:
        labels.append(("test-run", "FBCA04", "Development test issue; not official progress"))
    for name, color, description in labels:
        ensure_label(name, color, description)

    body = f"""# Day {day:03d} — {challenge['title']}

{challenge['title']} challenge.

**Challenge date:** {'Development test' if args.force_test else today.isoformat()}

## Scenario

Read the complete challenge instructions here:

[{challenge['file']}]({challenge['file']})

## Submission

1. Create your solution under `solutions/day-{day:03d}/`.
2. Add pytest tests and a short README.
3. Push your changes to the configured solution branch.
4. Comment `/submit` on this issue.
5. Review the feedback, then comment `/complete` when your work is ready.

---
{'**TEST ISSUE:** This issue is for workflow testing and is excluded from official progress.' if args.force_test else '**Official 100 Days of Code challenge.**'}
"""
    issue = post("issues", {
        "title": f"Day {day:03d}: {challenge['title']}",
        "body": body,
        "labels": [item[0] for item in labels],
    })
    print(f"Created challenge issue #{issue['number']}: {issue['html_url']}")


if __name__ == "__main__":
    main()
