# 100 Days of Code automation bundle — installation guide

This bundle is designed to be copied into the existing repository
`piyushv080/ai_and_automation_learning`. It does not replace your existing
`mkdocs.yml`, `requirements.txt`, README, or Pages workflow.

## 1. Copy files

Extract this bundle at the repository root and merge the `.github`,
`curriculum`, `docs`, and `tests` directories with the existing directories.

Do not overwrite `.github/workflows/pages.yml`.

## 2. Preserve your existing requirements

Add this line to the existing requirements.txt if pytest is not already present:

    pytest>=8,<10

Your existing MkDocs and theme dependencies must remain.

## 3. Add MkDocs navigation

Add these entries under the existing `nav:` key in mkdocs.yml. Preserve all
existing navigation entries and indentation:

    - 100 Days of Code:
        - Overview: 100-days-of-code/index.md
        - Day 001: 100-days-of-code/challenges/day-001.md
        - Day 002: 100-days-of-code/challenges/day-002.md
        - Day 003: 100-days-of-code/challenges/day-003.md

The overview page links all 100 challenge Markdown files. You can add the
remaining individual pages to navigation later if desired.

## 4. Install and test locally

    .venv/bin/python -m pip install pytest
    .venv/bin/python -m pytest -v
    .venv/bin/python -m compileall -q .github/scripts/100_days_of_code
    .venv/bin/python -m mkdocs build --strict

## 5. Feature branch

    git checkout feature/100-days-of-code
    git add .github curriculum docs/100-days-of-code tests pytest.ini
    git commit -m "feat: complete 100 days of code automation foundation"
    git push origin feature/100-days-of-code

## 6. Important GitHub Actions event limitation

GitHub `issue_comment` workflows are triggered only when the workflow file is
present on the repository's default branch. Therefore
`submission-validator.yml` and `challenge-completion.yml` can be developed and
tested on this feature branch, but their comment events will not run until the
workflow files are merged into the default branch.

The workflow checks out `feature/100-days-of-code` to run the scripts, but
that does not bypass the default-branch event requirement.

## 7. Testing challenge creation

In Actions, run "Daily 100 Days of Code Challenge" on the feature branch and
set `force_test` to true. This creates a clearly labeled `test-run` issue for
Day 001. Test issues are excluded from official progress.

Do not use force_test for the official launch. The normal scheduled run is
date-gated using curriculum/index.json and starts on 2026-11-15.

## 8. Launch safety

- GitHub Issues are repository-wide, not branch-specific.
- The issue-comment workflows need to be merged to the default branch before
  `/submit` and `/complete` events can trigger them.
- Update `SOLUTION_BRANCH` from feature/100-days-of-code to the chosen
  production solution branch before launch.
- The dispatcher uses GitHub's issue labels as progress state.
- The validator checks that a Python file exists; it does not execute or grade
  user code.
- `/complete` requires a successful submission-check comment and repository
  owner identity.
- The existing Pages workflow is not modified by this bundle.
