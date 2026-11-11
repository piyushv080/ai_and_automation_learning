
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_FILE = ROOT / "curriculum" / "index.json"


@pytest.fixture(scope="module")
def curriculum():
    """Load the challenge curriculum once for this test module."""

    assert CURRICULUM_FILE.is_file(), (
        f"Curriculum file not found: {CURRICULUM_FILE}"
    )

    with CURRICULUM_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def test_curriculum_file_is_valid_json():
    with CURRICULUM_FILE.open(encoding="utf-8") as file:
        data = json.load(file)

    assert isinstance(data, dict)


def test_curriculum_version_is_supported(curriculum):
    assert curriculum["version"] == 1


def test_total_days_is_100(curriculum):
    assert curriculum["total_days"] == 100


def test_challenges_are_defined(curriculum):
    assert len(curriculum["challenges"]) > 0


def test_challenge_days_are_unique(curriculum):
    days = [challenge["day"] for challenge in curriculum["challenges"]]

    assert len(days) == len(set(days))


def test_challenge_days_are_valid(curriculum):
    for challenge in curriculum["challenges"]:
        assert isinstance(challenge["day"], int)
        assert 1 <= challenge["day"] <= 100


def test_challenge_required_fields(curriculum):
    required_fields = {"day", "title", "file", "difficulty", "topics"}

    for challenge in curriculum["challenges"]:
        assert required_fields.issubset(challenge.keys())


def test_challenge_titles_are_not_empty(curriculum):
    for challenge in curriculum["challenges"]:
        assert challenge["title"].strip()


def test_challenge_files_exist(curriculum):
    for challenge in curriculum["challenges"]:
        challenge_file = ROOT / challenge["file"]

        assert challenge_file.is_file(), (
            f"Missing challenge file: {challenge_file}"
        )


def test_challenge_topics_are_defined(curriculum):
    for challenge in curriculum["challenges"]:
        assert isinstance(challenge["topics"], list)
        assert len(challenge["topics"]) > 0
