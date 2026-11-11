import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_FILE = ROOT / "curriculum" / "index.json"


@pytest.fixture(scope="module")
def curriculum():
    return json.loads(CURRICULUM_FILE.read_text(encoding="utf-8"))


def test_curriculum_has_100_days(curriculum):
    assert curriculum["total_days"] == 100
    assert len(curriculum["challenges"]) == 100


def test_days_are_exactly_1_to_100(curriculum):
    assert [item["day"] for item in curriculum["challenges"]] == list(range(1, 101))


def test_required_fields_exist(curriculum):
    required = {"day", "title", "file", "difficulty", "topics"}
    for item in curriculum["challenges"]:
        assert required.issubset(item)


def test_titles_and_topics_are_not_empty(curriculum):
    for item in curriculum["challenges"]:
        assert item["title"].strip()
        assert item["topics"]


def test_all_markdown_files_exist(curriculum):
    for item in curriculum["challenges"]:
        assert (ROOT / item["file"]).is_file()


def test_challenge_markdown_has_submission_instructions(curriculum):
    for item in curriculum["challenges"]:
        content = (ROOT / item["file"]).read_text(encoding="utf-8")
        assert "## Submission" in content
        assert "## Objectives" in content
