# GitHub Actions --- Complete CI/CD Learning Guide

> A practical, end-to-end guide to GitHub Actions for developers,
> infrastructure automation engineers, and platform/DevOps engineers.

**Official documentation:** https://docs.github.com/actions\
**GitHub Actions syntax:**
https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions\
**Learning goal:** Be able to design, write, debug, secure, and maintain
CI/CD workflows---not merely copy YAML.

------------------------------------------------------------------------

# 1. What is GitHub Actions?

GitHub Actions is GitHub's automation platform. It can automatically run
tasks when events happen in a repository or on a schedule.

Common uses:

-   Continuous Integration (CI): validate code, run tests, lint, scan,
    and build.
-   Continuous Delivery (CD): prepare and publish a deployable artifact.
-   Continuous Deployment: deploy automatically when configured
    conditions are met.
-   Infrastructure automation: validate Terraform, Ansible, Python,
    PowerShell, and shell changes.
-   Repository automation: label issues, publish releases, update
    documentation, and manage workflows.

A workflow is defined in a YAML file stored under:

``` text
.github/workflows/
```

Example:

``` text
my-project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
├── tests/
├── requirements.txt
└── README.md
```

GitHub Actions is event-driven: an event starts a workflow, the workflow
schedules jobs, and jobs run steps on runners.

------------------------------------------------------------------------

# 2. CI, Continuous Delivery, and Continuous Deployment

  -----------------------------------------------------------------------
  Concept                 Meaning                 Example
  ----------------------- ----------------------- -----------------------
  Continuous Integration  Frequently integrate    Run lint and unit tests
  (CI)                    changes and             on every pull request
                          automatically validate  
                          them                    

  Continuous Delivery     Keep changes validated  Build and publish a
                          and ready to release;   versioned artifact
                          production release may  
                          require approval        

  Continuous Deployment   Automatically deploy    Deploy to production
                          every change that       after protected checks
                          passes required checks  succeed
  -----------------------------------------------------------------------

A typical pipeline:

``` text
Developer change
      |
      v
Push branch / open pull request
      |
      v
Workflow trigger
      |
      v
Checkout source
      |
      v
Install dependencies
      |
      v
Lint + tests + security checks
      |
      v
Build artifact
      |
      v
Publish artifact
      |
      v
Approval / deployment policy
      |
      v
Deploy to target environment
      |
      v
Verify deployment and report status
```

Not every project needs every stage. Start with CI, then add packaging
and deployment once the checks are reliable.

------------------------------------------------------------------------

# 3. Core architecture and terminology

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  Workflow                            Complete automation definition in a
                                      YAML file

  Event                               Activity that triggers a workflow

  Trigger / `on`                      Event configuration in a workflow

  Job                                 Group of steps that runs on a
                                      runner

  Runner                              Machine/environment that executes a
                                      job

  Step                                Individual action or shell command
                                      within a job

  Action                              Reusable unit of automation

  Marketplace action                  Action published for reuse

  Composite action                    Multiple steps packaged as one
                                      action

  Reusable workflow                   A workflow called by another
                                      workflow

  Artifact                            File produced by a workflow and
                                      retained/uploaded

  Cache                               Stored dependency data reused to
                                      speed up later runs

  Environment                         Deployment target with protection
                                      rules and secrets

  Secret                              Sensitive value made available
                                      securely to a workflow

  Variable                            Non-sensitive configuration value

  Context                             Data exposed by GitHub, such as
                                      `github`, `runner`, `env`, `vars`,
                                      and `secrets`

  Expression                          Dynamic expression written as
                                      `${{ ... }}`

  Matrix                              Runs a job across multiple
                                      combinations

  Concurrency                         Controls overlapping workflow or
                                      job runs

  Status check                        Result used to decide whether a
                                      change can merge
  -----------------------------------------------------------------------

## Workflow execution model

1.  GitHub receives an event.
2.  GitHub evaluates the workflow's trigger filters.
3.  Eligible jobs are scheduled.
4.  Each job receives a runner.
5.  Steps execute in order unless conditions or failures alter the flow.
6.  Job results determine dependent job execution.
7.  Workflow status and artifacts are made available.

Jobs run in parallel by default unless dependencies are defined with
`needs`.

------------------------------------------------------------------------

# 4. Create your first workflow

Create `.github/workflows/hello.yml`:

``` yaml
name: Hello CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  hello:
    name: First job
    runs-on: ubuntu-latest

    steps:
      - name: Print message
        run: echo "Hello from GitHub Actions"

      - name: Show runner
        run: |
          echo "Operating system: $RUNNER_OS"
          echo "Repository: $GITHUB_REPOSITORY"
```

### Understand the input → logic → output

  Stage           Workflow example
  --------------- ---------------------------------------------------
  Input           A push or pull request targeting `main`
  Trigger logic   `on.push` and `on.pull_request` branch filters
  Runner          `ubuntu-latest`
  Steps           Print messages
  Output          Workflow run with success/failure status and logs

Commit and push the file. Open the repository's **Actions** tab to
inspect the run.

------------------------------------------------------------------------

# 5. Workflow YAML structure

A workflow usually contains:

``` yaml
name: Workflow name

on:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Step description
        run: echo "Hello"
```

  Key             Purpose
  --------------- ------------------------------------
  `name`          Human-readable workflow name
  `on`            Events and filters
  `permissions`   Token permissions
  `env`           Environment variables
  `defaults`      Default shell or working directory
  `concurrency`   Avoid unwanted overlapping runs
  `jobs`          Jobs in the workflow

YAML indentation matters. Use spaces, not tabs.

------------------------------------------------------------------------

# 6. Workflow triggers --- `on`

Triggers define when a workflow should run.

## 6.1 Push

``` yaml
on:
  push:
    branches:
      - main
      - 'release/**'
    paths:
      - 'src/**'
      - 'tests/**'
      - '.github/workflows/**'
```

Input: a push event, branch name, and changed paths.\
Logic: GitHub applies branch/path filters.\
Output: workflow starts only when filters match.

## 6.2 Pull request

``` yaml
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]
```

Use pull-request workflows to run checks before merging.

Important: pull-request workflows from forks have restricted token
permissions and secret availability. Do not try to bypass these
protections.

## 6.3 Manual trigger --- `workflow_dispatch`

``` yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: Target environment
        required: true
        type: choice
        options:
          - dev
          - test
      dry_run:
        description: Preview changes only
        required: true
        type: boolean
        default: true
```

The workflow can read the input using:

``` yaml
${{ inputs.environment }}
${{ inputs.dry_run }}
```

Validate inputs and use allowlists. A manual trigger does not
automatically make a deployment safe.

## 6.4 Schedule

``` yaml
on:
  schedule:
    - cron: '30 2 * * 1-5'
```

Scheduled workflows use UTC. They may be delayed during high load. Do
not rely on schedules for precise timing or critical real-time
operations.

## 6.5 Other useful events

-   `release`: release published or changed.
-   `workflow_dispatch`: manually run a workflow.
-   `workflow_call`: reusable workflow invocation.
-   `workflow_run`: after another workflow completes.
-   `issues`: issue activity.
-   `issue_comment`: issue or pull request comment.
-   `create`: branch or tag created.
-   `delete`: branch or tag deleted.
-   `repository_dispatch`: external system sends a repository event.
-   `merge_group`: merge queue validation.
-   `pull_request_target`: privileged pull request event; requires
    special security care.

Use only events needed by the workflow.

------------------------------------------------------------------------

# 7. Jobs, steps, runners, and shells

## 7.1 Jobs

``` yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Linting"

  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Testing"
```

These jobs may run in parallel.

## 7.2 Job dependencies --- `needs`

``` yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Tests passed"

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: echo "Build after tests"
```

`build` runs only after `test` succeeds, unless an explicit condition
changes the default behavior.

## 7.3 Runners

Common GitHub-hosted runner labels include:

-   `ubuntu-latest`
-   `windows-latest`
-   `macos-latest`

Use a self-hosted runner only when there is a clear requirement, such as
private network access or specialized hardware. Treat it as a privileged
machine: isolate it, restrict who can schedule jobs on it, patch it, and
avoid exposing it to untrusted pull requests.

## 7.4 Shell selection

``` yaml
- name: Bash
  shell: bash
  run: echo "Linux/macOS shell"

- name: PowerShell
  shell: pwsh
  run: Write-Output "PowerShell step"

- name: Python
  shell: bash
  run: python --version
```

Specify the shell when portability and predictable behavior matter.

------------------------------------------------------------------------

# 8. Steps: `run`, `uses`, `with`, `env`, and `working-directory`

A step can run a shell command or call an action.

## 8.1 `run`

``` yaml
- name: Show files
  run: ls -la
```

## 8.2 `uses`

``` yaml
- name: Checkout source
  uses: actions/checkout@v4
```

`uses` invokes an action. Review its source, permissions, maintenance,
and release history. Pin third-party actions to a verified full commit
SHA for stronger supply-chain protection; use a trusted versioning
policy for first-party actions.

## 8.3 `with`

Passes action inputs:

``` yaml
- name: Checkout
  uses: actions/checkout@v4
  with:
    fetch-depth: 1
```

## 8.4 `env`

``` yaml
env:
  APP_ENV: test

jobs:
  example:
    runs-on: ubuntu-latest
    steps:
      - name: Print environment
        run: echo "Environment is $APP_ENV"
```

Do not put secrets in plain environment variables or print them.

## 8.5 `working-directory`

``` yaml
- name: Run tests
  working-directory: ./app
  run: python -m pytest
```

------------------------------------------------------------------------

# 9. Contexts, expressions, and variables

Expressions use `${{ ... }}`.

Common contexts:

  Context      Purpose
  ------------ -----------------------------------------------------
  `github`     Repository, event, ref, actor, SHA and run metadata
  `env`        Workflow/job/step environment variables
  `vars`       Repository, organization, or environment variables
  `secrets`    Secret values
  `runner`     Runner metadata
  `job`        Current job information
  `steps`      Outputs and outcomes of earlier steps
  `needs`      Outputs and results of dependent jobs
  `matrix`     Current matrix combination
  `inputs`     Workflow dispatch or reusable workflow inputs
  `strategy`   Matrix/fail-fast strategy data

Examples:

``` yaml
- name: Show commit
  run: echo "Commit $GITHUB_SHA"

- name: Show actor
  run: echo "Actor: ${{ github.actor }}"
```

Use expressions in workflow fields that support them. Be careful when
inserting untrusted values into shell commands. Prefer passing values
through environment variables and quoting them safely.

## Common expression functions

-   `contains(search, item)`
-   `startsWith(search, searchString)`
-   `endsWith(search, searchString)`
-   `format(string, args...)`
-   `join(array, separator)`
-   `toJSON(value)`
-   `fromJSON(value)`
-   `hashFiles(path...)`

## Status functions

-   `success()`
-   `failure()`
-   `always()`
-   `cancelled()`

Example:

``` yaml
- name: Collect diagnostics
  if: ${{ always() }}
  run: echo "Collect diagnostics even after earlier failure"
```

Use `always()` carefully. A cleanup or diagnostic step should not
accidentally hang indefinitely.

------------------------------------------------------------------------

# 10. Outputs and sharing data between steps/jobs

## 10.1 Step outputs

Write to `$GITHUB_OUTPUT`:

``` yaml
steps:
  - name: Create output
    id: metadata
    run: echo "version=1.2.3" >> "$GITHUB_OUTPUT"

  - name: Read output
    env:
      APP_VERSION: ${{ steps.metadata.outputs.version }}
    run: echo "Version: $APP_VERSION"
```

Input: a value created in one step.\
Processing: write a named output to the runner-provided output file.\
Output: a value available to later steps.

## 10.2 Job outputs

``` yaml
jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.meta.outputs.version }}
    steps:
      - id: meta
        run: echo "version=1.2.3" >> "$GITHUB_OUTPUT"

  deploy:
    needs: prepare
    runs-on: ubuntu-latest
    steps:
      - env:
          VERSION: ${{ needs.prepare.outputs.version }}
        run: echo "Deploying $VERSION"
```

Do not use outputs to transport secrets. Use secrets or a suitable
secret manager.

------------------------------------------------------------------------

# 11. Artifacts and caching

These solve different problems.

## 11.1 Artifacts

Artifacts preserve workflow outputs, such as test reports, packages, or
build files.

``` yaml
- name: Upload report
  uses: actions/upload-artifact@v4
  with:
    name: test-report
    path: reports/
    if-no-files-found: error
    retention-days: 7
```

Download in another job:

``` yaml
- name: Download report
  uses: actions/download-artifact@v4
  with:
    name: test-report
    path: reports/
```

Artifact input: files created by a job.\
Output: stored artifact accessible according to retention and
permissions.

Do not upload credentials, private keys, or sensitive production data.

## 11.2 Dependency cache

Caching speeds up repeated dependency installation. It is not a
substitute for an artifact or a source of truth.

Example using `actions/setup-python` cache support:

``` yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: pip
    cache-dependency-path: requirements.txt
```

Use cache keys that reflect dependency files and relevant runtime
configuration. Do not cache secrets.

------------------------------------------------------------------------

# 12. Matrix builds

A matrix repeats a job across a set of combinations.

``` yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.11', '3.12', '3.13']

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - run: python --version
```

Input: matrix values.\
Logic: GitHub creates a job for each combination.\
Output: independent results per combination.

Use matrices for Python versions, operating systems, Terraform versions,
or supported deployment targets. Avoid an unnecessarily large matrix
that increases runtime and cost.

------------------------------------------------------------------------

# 13. Reusable workflows and composite actions

## 13.1 Reusable workflow

A reusable workflow is a complete workflow called by another workflow.

Caller:

``` yaml
jobs:
  call-validation:
    uses: ./.github/workflows/reusable-validation.yml
    with:
      python-version: '3.12'
```

Reusable workflow:

``` yaml
name: Reusable Python validation

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
      - run: python --version
```

Use reusable workflows when multiple repositories need the same CI/CD
process.

## 13.2 Composite action

A composite action packages multiple steps into one reusable action. It
is commonly defined in `action.yml`.

``` yaml
name: Example greeting
description: Print a greeting
inputs:
  name:
    description: Name to greet
    required: true

runs:
  using: composite
  steps:
    - name: Print greeting
      shell: bash
      run: echo "Hello ${{ inputs.name }}"
```

Use environment variables rather than directly interpolating untrusted
inputs into shell source in production-quality actions.

------------------------------------------------------------------------

# 14. Conditions, failure handling, and execution control

## 14.1 `if`

``` yaml
- name: Deploy only from main
  if: github.ref == 'refs/heads/main'
  run: echo "Deployment stage"
```

## 14.2 Continue on error

``` yaml
- name: Optional diagnostic
  continue-on-error: true
  run: ./collect-diagnostics.sh
```

Use this only for non-critical steps. Do not hide failures in required
validation or deployment steps.

## 14.3 Timeouts

``` yaml
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
```

Set realistic timeouts to prevent hung jobs.

## 14.4 Concurrency

``` yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: true
```

For deployments, choose concurrency behavior carefully. Cancelling a
deployment while it is changing infrastructure may be unsafe. Use
serialization where appropriate.

## 14.5 Job result behavior

A failed job normally prevents dependent jobs from running. Use `needs`,
`if`, and status functions deliberately. A deployment job should depend
on all required validation jobs.

------------------------------------------------------------------------

# 15. Permissions and `GITHUB_TOKEN`

The workflow token is automatically provided by GitHub. Grant only the
permissions needed.

Example read-only workflow:

``` yaml
permissions:
  contents: read
```

Example publishing workflow may need a narrowly scoped permission such
as:

``` yaml
permissions:
  contents: read
  packages: write
```

Common permissions include:

-   `contents`
-   `packages`
-   `pull-requests`
-   `issues`
-   `checks`
-   `actions`
-   `id-token`

Use the smallest permission set possible. Set permissions at workflow or
job level. A job can receive a narrower set than the workflow.

Never print `${{ secrets.GITHUB_TOKEN }}` or any secret. Avoid passing
secrets through command-line arguments where they may appear in process
listings or logs.

------------------------------------------------------------------------

# 16. Secrets, variables, and environments

## 16.1 Secrets

Use repository, organization, or environment secrets for credentials.

``` yaml
- name: Use API token
  env:
    API_TOKEN: ${{ secrets.API_TOKEN }}
  run: |
    python scripts/check_api.py
```

The script should read the environment variable securely and never print
it.

## 16.2 Variables

Use `vars` for non-sensitive configuration:

``` yaml
env:
  TARGET_REGION: ${{ vars.TARGET_REGION }}
```

Do not store passwords, access tokens, or private keys in variables.

## 16.3 Environments

Environments can provide: - Environment-specific secrets and
variables. - Required reviewers and deployment protection rules. -
Deployment history.

``` yaml
jobs:
  deploy:
    environment: test
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to approved test environment"
```

Use protected environments for production deployments.

------------------------------------------------------------------------

# 17. Complete Python CI workflow

Example repository:

``` text
python-automation/
├── .github/workflows/python-ci.yml
├── src/
│   └── healthcheck.py
├── tests/
│   └── test_healthcheck.py
├── requirements.txt
└── README.md
```

Workflow:

``` yaml
name: Python CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip
          cache-dependency-path: requirements.txt

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt
          python -m pip install pytest

      - name: Compile source
        run: python -m compileall -q src tests

      - name: Run tests
        run: python -m pytest -q
```

**Input:** Code changes and dependency definitions.\
**Logic:** Set up Python, install packages, compile, and test.\
**Output:** Successful or failed CI check.

For reproducible builds, pin or constrain dependencies using a suitable
dependency-management strategy.

------------------------------------------------------------------------

# 18. Complete PowerShell CI workflow

``` yaml
name: PowerShell CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: windows-latest

    steps:
      - uses: actions/checkout@v4

      - name: Check PowerShell version
        shell: pwsh
        run: $PSVersionTable.PSVersion.ToString()

      - name: Run PSScriptAnalyzer
        shell: pwsh
        run: |
          Install-Module PSScriptAnalyzer -Scope CurrentUser -Force
          Invoke-ScriptAnalyzer -Path ./scripts -Recurse -Severity Error

      - name: Run Pester tests
        shell: pwsh
        run: |
          Install-Module Pester -Scope CurrentUser -Force
          Invoke-Pester -Path ./tests -CI
```

Input: PowerShell scripts and tests.\
Logic: Analyze scripts and execute Pester tests.\
Output: Lint/test results.

In production, use controlled module versions and dependency caching
where useful.

------------------------------------------------------------------------

# 19. Terraform CI workflow

A validation pipeline can run formatting, initialization, validation,
and a plan.

``` yaml
name: Terraform Validation

on:
  pull_request:
    paths:
      - 'terraform/**'
      - '.github/workflows/terraform.yml'

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: terraform

    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: '1.9.8'

      - name: Format check
        run: terraform fmt -check -recursive

      - name: Initialize
        run: terraform init -backend=false

      - name: Validate
        run: terraform validate
```

This example validates configuration without configuring a real remote
backend. A real plan may require provider credentials and backend
access; use a separate, protected workflow and least-privilege identity.

Do not automatically apply infrastructure from untrusted pull requests.
Require plan review and protected deployment approval.

------------------------------------------------------------------------

# 20. Ansible CI workflow

``` yaml
name: Ansible Validation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Ansible
        run: python -m pip install ansible-core

      - name: Check Ansible version
        run: ansible --version

      - name: Syntax check
        run: ansible-playbook -i inventory/test.ini playbooks/site.yml --syntax-check
```

Use a non-production inventory and avoid exposing production credentials
to pull-request jobs.

Additional validation tools can include `ansible-lint` and YAML linting.

------------------------------------------------------------------------

# 21. Docker CI workflow

``` yaml
name: Docker Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t sample-app:${{ github.sha }} .

      - name: Inspect image
        run: docker image inspect sample-app:${{ github.sha }}
```

This validates that the image builds. Add image scanning, tests,
registry publishing, and deployment as separate controlled stages.

------------------------------------------------------------------------

# 22. CD deployment workflow pattern

A deployment workflow should separate validation from deployment and
protect the target environment.

``` yaml
name: Deploy to test

on:
  workflow_dispatch:
    inputs:
      release:
        description: Release identifier
        required: true
        type: string

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate release input
        env:
          RELEASE: ${{ inputs.release }}
        run: |
          test -n "$RELEASE"
          echo "Release input provided"

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    environment: test
    steps:
      - name: Deployment placeholder
        env:
          RELEASE: ${{ inputs.release }}
        run: |
          echo "Deployment would run for release: $RELEASE"
```

This is a structural example, not a real deployment. Replace the
placeholder only after defining: - Target platform and authentication. -
Approved deployment command. - Artifact provenance. - Rollback
strategy. - Health verification. - Deployment permissions and approvals.

Never treat a successful workflow step as proof that the application is
healthy.

------------------------------------------------------------------------

# 23. OpenID Connect (OIDC) for cloud authentication

OIDC can allow GitHub Actions to obtain short-lived cloud credentials
without storing long-lived cloud access keys as GitHub secrets.

Typical flow:

1.  Configure an identity trust relationship in the cloud provider.
2.  Restrict it to the intended GitHub organization, repository, branch,
    and/or environment.
3.  Give the workflow `id-token: write`.
4.  Use the provider's official login action or SDK flow.
5.  Grant only required cloud permissions.
6.  Verify the identity and target account before deployment.

Example permission declaration:

``` yaml
permissions:
  contents: read
  id-token: write
```

`id-token: write` permits requesting an OIDC token; it does not by
itself grant cloud-resource access. Cloud-side trust and IAM permissions
must also be configured.

------------------------------------------------------------------------

# 24. Security best practices

Treat CI/CD workflows as production code.

## Essential controls

-   Use least-privilege `permissions`.
-   Pin third-party actions to verified full commit SHAs where
    practical.
-   Review action source and updates.
-   Keep secrets out of source code, logs, artifacts, and command-line
    arguments.
-   Use protected environments and required reviewers for production.
-   Avoid running privileged workflows on untrusted fork code.
-   Do not use `pull_request_target` casually.
-   Avoid interpolating untrusted event data directly into shell
    scripts.
-   Use environment variables and safe argument handling.
-   Set timeouts and concurrency controls.
-   Use OIDC and short-lived credentials where supported.
-   Scan dependencies and build artifacts.
-   Keep self-hosted runners isolated and patched.
-   Limit artifact retention and access.
-   Review workflow changes as carefully as application code.

## Untrusted input example

Risky pattern:

``` yaml
- run: echo "${{ github.event.pull_request.title }}"
```

The pull request title is untrusted input and is inserted into shell
source.

Safer pattern:

``` yaml
- name: Print pull request title
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    printf '%s\n' "$PR_TITLE"
```

Passing data through an environment variable avoids direct insertion
into the script source. Continue to quote variables and validate data
before using it in commands.

------------------------------------------------------------------------

# 25. Debugging and troubleshooting

  -----------------------------------------------------------------------
  Symptom                 Possible cause          What to inspect
  ----------------------- ----------------------- -----------------------
  Workflow does not start Trigger or branch/path  `on` configuration and
                          filter mismatch         event

  YAML error              Invalid indentation or  Workflow editor and
                          syntax                  YAML parser

  Action not found        Incorrect action        `uses` value and action
                          name/ref                repository

  Permission denied       Token or runner         `permissions`, identity
                          permissions             and filesystem
                          insufficient            

  Secret is empty         Secret unavailable to   Secret scope, fork
                          event/environment       restrictions,
                                                  environment

  Job skipped             Failed dependency or    `needs`, job result and
                          false `if` condition    expression

  Command not found       Tool missing from       Install/setup step and
                          runner                  PATH

  Test passes locally but OS, runtime,            Runner OS, versions,
  fails in CI             dependency, path or     locale and
                          environment difference  configuration

  API request fails       Network,                Response status, safe
                          authentication, TLS,    logs and endpoint
                          timeout or API status   

  Deployment overlaps     Concurrent runs         `concurrency` and
                                                  environment controls

  Artifact missing        Wrong path or upload    Working directory, file
                          step skipped            existence and step
                                                  condition
  -----------------------------------------------------------------------

## Debugging procedure

1.  Open the repository's Actions tab.
2.  Select the failed workflow run.
3.  Open the failed job and step.
4.  Read the first meaningful error, not only the final failure line.
5.  Identify whether the problem is YAML, permissions, dependency,
    command, network, or application logic.
6.  Reproduce locally where possible.
7.  Fix the smallest cause.
8.  Push a new change and verify the complete workflow.

Do not print secrets or enable verbose logging that may expose
credentials.

------------------------------------------------------------------------

# 26. Workflow commands and environment files

GitHub provides runner file paths for communicating between steps.

  File / command                 Purpose
  ------------------------------ -------------------------------------------
  `$GITHUB_OUTPUT`               Set step outputs
  `$GITHUB_ENV`                  Set environment variables for later steps
  `$GITHUB_PATH`                 Add paths to PATH for later steps
  `$GITHUB_STEP_SUMMARY`         Add Markdown to the job summary
  `::notice::`                   Create notice annotation
  `::warning::`                  Create warning annotation
  `::error::`                    Create error annotation
  `::group::` / `::endgroup::`   Group log output

Example:

``` yaml
- name: Set environment variable
  run: echo "APP_ENV=test" >> "$GITHUB_ENV"

- name: Use variable
  run: echo "$APP_ENV"
```

Example job summary:

``` yaml
- name: Write summary
  run: |
    echo "## CI result" >> "$GITHUB_STEP_SUMMARY"
    echo "- Tests completed" >> "$GITHUB_STEP_SUMMARY"
```

Use the documented environment-file mechanism rather than deprecated
workflow command patterns.

------------------------------------------------------------------------

# 27. CI/CD workflow design checklist

Before merging a workflow, ask:

-   [ ] Does the workflow run on the correct events?
-   [ ] Are branch and path filters correct?
-   [ ] Are runner OS and tool versions intentional?
-   [ ] Are dependencies installed reproducibly?
-   [ ] Are linting and tests included?
-   [ ] Are job dependencies correct?
-   [ ] Are outputs and artifacts used appropriately?
-   [ ] Are timeouts configured?
-   [ ] Are token permissions minimal?
-   [ ] Are secrets protected?
-   [ ] Are untrusted inputs handled safely?
-   [ ] Are actions and dependencies reviewed?
-   [ ] Are production environments protected?
-   [ ] Is there a rollback or recovery plan?
-   [ ] Is deployment verified after execution?
-   [ ] Are logs useful but free of secrets?

------------------------------------------------------------------------

# 28. Hands-on learning roadmap

## Level 1 --- Workflow fundamentals

1.  Create a workflow that runs on push.
2.  Add a pull-request trigger.
3.  Print repository, branch, and commit metadata.
4.  Create two jobs.
5.  Make the second job depend on the first.
6.  Add a manual workflow trigger.
7.  Add an environment variable and step output.

## Level 2 --- Python CI

1.  Create a small Python project.
2.  Add a requirements file.
3.  Configure Python on a runner.
4.  Install dependencies.
5.  Run compilation and unit tests.
6.  Upload a test report.
7.  Add a matrix for two or more Python versions.

## Level 3 --- Infrastructure validation

1.  Add Terraform formatting and validation.
2.  Add Ansible syntax checking.
3.  Add PowerShell static analysis and tests.
4.  Add shell syntax checking.
5.  Add a Docker image build.
6.  Publish a safe build artifact.

## Level 4 --- Secure delivery

1.  Configure a protected test environment.
2.  Add environment-specific variables.
3.  Add required reviewers where appropriate.
4.  Configure minimal token permissions.
5.  Configure cloud OIDC in a sandbox.
6.  Add deployment and post-deployment verification.
7.  Document rollback and incident procedures.

## Level 5 --- Reusable platform engineering

1.  Create a reusable Python CI workflow.
2.  Create a reusable infrastructure validation workflow.
3.  Create a composite action for a repeated task.
4.  Add workflow concurrency controls.
5.  Create a release workflow.
6.  Add artifact provenance and security scanning.
7.  Document a complete delivery process.

------------------------------------------------------------------------

# 29. Capstone project: Infrastructure Automation CI/CD

Build a repository with this structure:

``` text
infrastructure-automation/
├── .github/
│   └── workflows/
│       ├── python-ci.yml
│       ├── ansible-validation.yml
│       ├── terraform-validation.yml
│       └── deploy-test.yml
├── python/
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── ansible/
│   ├── inventory/
│   └── playbooks/
├── terraform/
├── scripts/
│   ├── health_check.sh
│   └── health_check.ps1
└── README.md
```

### Required behavior

**On pull request** - Run Python tests. - Run PowerShell and shell
checks. - Validate Ansible syntax. - Validate Terraform formatting and
configuration. - Build container image if applicable. - Publish test
reports. - Do not deploy production infrastructure.

**On merge to main** - Build versioned artifacts. - Run required
security and quality checks. - Publish approved artifacts.

**On manual deployment request** - Validate release and target inputs. -
Require protected environment approval. - Authenticate using short-lived
credentials where possible. - Deploy only the approved artifact. - Run
health checks. - Report deployment status and recovery instructions.

### Acceptance criteria

-   Every required check is visible in the pull request.
-   A failed required check prevents the protected merge.
-   Secrets are not exposed to untrusted jobs.
-   Production deployment requires the configured protection rules.
-   A deployment is considered successful only after verification.
-   A failed deployment has a documented recovery path.

------------------------------------------------------------------------

# 30. Interview preparation questions

1.  What is GitHub Actions?
2.  What is the difference between CI and CD?
3.  What is a workflow, job, step, action, and runner?
4.  What is the difference between `run` and `uses`?
5.  What does `needs` do?
6.  What is a matrix strategy?
7.  What are contexts and expressions?
8.  How do you share data between steps?
9.  What is the difference between an artifact and a cache?
10. What is a reusable workflow?
11. What is a composite action?
12. How do you secure `GITHUB_TOKEN`?
13. How do repository secrets differ from environment secrets?
14. What are protected environments?
15. How does OIDC work with cloud providers?
16. Why should third-party actions be pinned and reviewed?
17. How do you prevent untrusted pull-request code from accessing
    secrets?
18. How do you troubleshoot a failed workflow?
19. How do you prevent overlapping deployments?
20. How do you verify a deployment succeeded?
21. How would you build CI for Python?
22. How would you validate Terraform and Ansible?
23. How would you publish and deploy a versioned artifact?
24. How would you implement rollback?
25. How would you design a secure infrastructure automation pipeline?

------------------------------------------------------------------------

# 31. Official documentation and references

Use official documentation as the source of truth. GitHub changes runner
images, action versions, and workflow capabilities over time.

-   GitHub Actions overview: https://docs.github.com/actions
-   Workflow syntax:
    https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions
-   Events that trigger workflows:
    https://docs.github.com/actions/using-workflows/events-that-trigger-workflows
-   Workflow expressions:
    https://docs.github.com/actions/learn-github-actions/expressions
-   Contexts:
    https://docs.github.com/actions/learn-github-actions/contexts
-   Variables:
    https://docs.github.com/actions/learn-github-actions/variables
-   Secrets:
    https://docs.github.com/actions/security-guides/using-secrets-in-github-actions
-   Security hardening:
    https://docs.github.com/actions/security-guides/security-hardening-for-github-actions
-   OIDC:
    https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect
-   Artifacts:
    https://docs.github.com/actions/using-workflows/storing-workflow-data-as-artifacts
-   Dependency caching:
    https://docs.github.com/actions/using-workflows/caching-dependencies-to-speed-up-workflows
-   Reusable workflows:
    https://docs.github.com/actions/using-workflows/reusing-workflows
-   Composite actions:
    https://docs.github.com/actions/creating-actions/creating-a-composite-action
-   Self-hosted runners:
    https://docs.github.com/actions/hosting-your-own-runners
-   GitHub Actions billing:
    https://docs.github.com/billing/managing-billing-for-github-actions

------------------------------------------------------------------------

## Final learning principle

A good CI/CD engineer understands more than YAML syntax.

You should be able to explain:

-   What event starts the workflow.
-   What input each job receives.
-   What logic each step performs.
-   What permissions the workflow needs.
-   What artifacts it creates.
-   What happens when a step fails.
-   How deployment is authorized.
-   How the final state is verified.

**Build pipelines that are repeatable, secure, observable, and
recoverable.**