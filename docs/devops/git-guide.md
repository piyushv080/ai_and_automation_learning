# Git Guide

Git is a distributed version control system created by Linus Torvalds in 2005 to manage the Linux kernel source tree. It records snapshots of a project, lets many people work on the same codebase, and makes it possible to review, compare, merge, and undo changes safely.

## Version control concepts

A **version control system (VCS)** tracks changes to files over time. It lets you answer questions such as:

- What changed, when, and by whom?
- Why was a change made?
- How do I restore an earlier version?
- How do I combine work from multiple people?

Common VCS models:

| Model | Description | Examples |
| --- | --- | --- |
| Local | History is stored only on one machine. | RCS |
| Centralized | One server holds the authoritative history. | CVS, Subversion |
| Distributed | Every clone contains the full history. | Git, Mercurial |

Git is distributed: most operations are local, commits are cheap, and a clone can work independently before synchronizing with a remote.

## Why Git

- **Fast:** most commands read local data and do not need a network connection.
- **Distributed:** every clone has the complete project history.
- **Branch-friendly:** creating and switching branches is inexpensive.
- **Content-addressed:** objects are identified by cryptographic hashes, which helps detect corruption.
- **Flexible workflows:** supports small teams, large open-source projects, and automated delivery pipelines.
- **Integrates well:** GitHub, GitLab, Bitbucket, Azure DevOps, and CI/CD tools all support Git.

Git does not automatically enforce a workflow. Teams must agree on branch naming, review rules, merge or rebase policy, release tagging, and access control.

## Core terminology

| Term | Meaning |
| --- | --- |
| Repository | The project database plus its configuration and history. |
| Working tree | The checked-out files you edit. |
| Index / staging area | The proposed next commit. |
| Commit | A snapshot with metadata, a message, and parent commit references. |
| Branch | A movable reference to a commit. |
| Tag | A fixed reference to a commit, commonly used for releases. |
| `HEAD` | A reference to the current branch or commit. |
| Remote | Another repository, often hosted on a server. |
| `origin` | The conventional name for the remote a repository was cloned from. |
| `upstream` | A common name for the original repository when working from a fork. |
| Blob | A Git object containing file contents. |
| Tree | A Git object representing a directory snapshot. |
| Commit object | A Git object containing a tree, parent commits, author, committer, and message. |
| Annotated tag | A tag object with a message and tagger metadata. |
| Object ID | A hash identifying a Git object. |
| Revision | A way to identify a commit, such as a branch, tag, or abbreviated hash. |

Git object IDs are SHA-1 by default in most existing repositories. Repositories using SHA-256 are also supported. Do not assume a fixed hash length in scripts.

## How Git stores changes

Git stores snapshots, not a simple sequence of file diffs. Each commit points to a tree that describes the project at that moment. Trees point to blobs for file contents and to other trees for subdirectories.

```text
commit -> tree -> blob
              -> tree -> blob
```

Branches and tags are references into this object graph. When you commit, Git creates new objects and moves the current branch reference forward.

## The three main states

Files move through three main areas:

```text
Working tree  --git add-->  Index / staging area  --git commit-->  Local repository
       ^                                                                    |
       |                                                                    |
       +-------------------------- git checkout / restore ----------------+
```

- **Modified:** the working tree differs from the last commit.
- **Staged:** the change is in the index and will be included in the next commit.
- **Committed:** the snapshot is stored in the local repository.

A remote repository adds another synchronization step:

```text
Local repository  --git push-->  Remote repository
Local repository  <--git fetch/pull--  Remote repository
```

## Install and configure Git

Install Git with your operating system package manager, then confirm the version:

```bash
git --version
```

Minimum configuration:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.test"
git config --global init.defaultBranch main
```

Useful settings:

```bash
git config --global core.editor "vim"
git config --global color.ui auto
git config --global pull.rebase true
git config --global fetch.prune true

# Linux and macOS: convert CRLF to LF when committing
git config --global core.autocrlf input

# Windows: check out CRLF and commit LF
# git config --global core.autocrlf true
```

Inspect configuration and find where each value comes from:

```bash
git config --list
git config --list --show-origin
git config --get user.email
```

Configuration scopes:

- `--local`: this repository only, stored in `.git/config`.
- `--global`: the current user, stored in the user's Git configuration file.
- `--system`: all users on the machine.

Precedence is local, then global, then system.

## Create a repository

Initialize a new repository in the current directory:

```bash
mkdir example-project
cd example-project
git init
```

Stage files and create the first commit:

```bash
git status
git add README.md
git commit -m "Add project README"
```

Create a repository with a specific initial branch:

```bash
git init --initial-branch=main
```

## Clone a repository

```bash
git clone https://github.com/example-org/example-repo.git
git clone git@github.com:example-org/example-repo.git
git clone https://github.com/example-org/example-repo.git custom-directory
```

Useful clone options:

```bash
# Shallow clone: faster, but limited history
git clone --depth 1 https://github.com/example-org/example-repo.git

# Clone a specific branch
git clone --branch release/1.0 https://github.com/example-org/example-repo.git
```

A clone creates a local repository, checks out the default branch, and records the source as `origin`.

## Everyday workflow

Check status before and after making changes:

```bash
git status
git status -sb
```

Review changes:

```bash
git diff                     # unstaged changes
git diff --staged            # staged changes
git diff HEAD                # all changes since the last commit
git diff --stat
```

Stage changes:

```bash
git add file.txt
git add src/ tests/
git add .
git add -p                   # review and stage selected hunks
```

Commit:

```bash
git commit -m "Describe the change"
git commit -am "Describe the change"   # tracked files only
git commit                             # opens the configured editor
```

Review history:

```bash
git log
git log --oneline
git log --oneline --graph --decorate --all
git log --author="Your Name"
git log --since="2 weeks ago"
git show HEAD
git show <commit>
```

A good commit message is short, specific, and usually written in the imperative mood, for example `Fix timeout handling in upload retry`.

## Synchronize with a remote

List and inspect remotes:

```bash
git remote -v
git remote show origin
```

Add or change a remote:

```bash
git remote add origin https://github.com/example-org/example-repo.git
git remote set-url origin git@github.com:example-org/example-repo.git
git remote rename origin upstream
git remote remove old-remote
```

Download remote updates without changing the working tree:

```bash
git fetch origin
git fetch --prune
```

Integrate remote changes:

```bash
git pull
git pull --rebase
git pull --ff-only
```

Push local commits:

```bash
git push
git push -u origin main
git push origin feature/my-change
```

`-u` sets the upstream branch so later commands can use plain `git push` and `git pull`.

For HTTPS remotes, use a credential manager or a personal access token. Do not use an account password where the hosting provider requires a token. SSH keys are often more convenient for development machines.

## Undo and fix mistakes

### Amend the last commit

```bash
git commit --amend --no-edit
git commit --amend -m "Corrected commit message"
```

Only amend commits that have not been shared, unless your team explicitly allows history rewrites.

### Unstage a file

```bash
git restore --staged file.txt
# Older equivalent:
git reset HEAD file.txt
```

### Discard working tree changes

```bash
git restore file.txt
# Older equivalent:
git checkout -- file.txt
```

This discards uncommitted edits. Use it deliberately.

### Reset a branch

```bash
git reset --soft HEAD~1
git reset HEAD~1
git reset --hard HEAD~1
```

- `--soft` moves the branch but keeps changes staged.
- `--mixed` (the default) moves the branch and unstages changes while keeping the working tree.
- `--hard` moves the branch and discards both staged and unstaged changes.

`--hard` is destructive. Check `git status` and `git diff` first.

### Revert a commit safely

```bash
git revert <commit>
git revert --no-commit <commit>
git revert --continue
git revert --abort
```

`git revert` creates a new commit that reverses an earlier change, so it is suitable for shared branches.

### Recover lost work

The reflog records recent branch and `HEAD` movements:

```bash
git reflog
git reset --hard HEAD@{1}
```

The reflog is local and eventually expires. Commit work early and push important branches to a remote.

## Stash temporary work

Stashing saves uncommitted changes and restores a clean working tree:

```bash
git stash push -m "Work in progress"
git stash list
git stash show -p
git stash apply
git stash pop
git stash drop
```

Include untracked or ignored files when needed:

```bash
git stash push -u
git stash push -a
```

Create a branch from a stash:

```bash
git stash branch fix/from-stash
```

Prefer a temporary commit on a branch for work that must not be lost.

## Move, rename, and delete files

```bash
git mv old-name.txt new-name.txt
git mv src/old-module src/new-module
git rm obsolete.txt
git rm -r old-directory
```

Stop tracking a file but keep it locally:

```bash
git rm --cached local-settings.env
```

Add the path to `.gitignore` when it should never be committed again.

## Tags and releases

List tags:

```bash
git tag
git tag -l "v2.*"
```

Create an annotated release tag:

```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git show v1.0.0
```

Push tags:

```bash
git push origin v1.0.0
git push origin --tags
```

Delete tags:

```bash
git tag -d v1.0.0
git push origin --delete v1.0.0
```

Use annotated tags for releases. Prefer semantic versioning such as `v1.4.2`, and treat published tags as immutable.

## Patches

Patches are useful when changes must move between repositories without a direct remote connection.

Create email-formatted patches:

```bash
git format-patch -1 <commit>
git format-patch main..feature/my-change
git format-patch --stdout main..feature/my-change > changes.patch
```

Apply patches:

```bash
git apply --check changes.patch
git apply changes.patch
git am 0001-describe-the-change.patch
```

`git format-patch` plus `git am` preserves commit metadata. A plain `git diff > changes.patch` produces a patch without commit metadata, which `git apply` can still apply.

## Branches

List branches:

```bash
git branch
git branch -a
git branch -vv
```

Create and switch:

```bash
git branch feature/my-change
git switch feature/my-change

git switch -c feature/my-change
# Older equivalent:
git checkout -b feature/my-change
```

Rename and delete:

```bash
git branch -m old-name new-name
git branch -d feature/my-change
git branch -D feature/my-change
```

Push and delete remote branches:

```bash
git push -u origin feature/my-change
git push origin --delete feature/my-change
git fetch --prune
```

Use descriptive branch names such as `feature/login-validation`, `fix/timeout-retry`, or `release/2.1`.

## Merging

Merge another branch into the current branch:

```bash
git switch main
git pull --ff-only
git merge feature/my-change
```

Merge types:

- **Fast-forward:** the target branch has no new commits, so the branch pointer simply moves forward.
- **Three-way merge:** both branches have diverged, so Git combines the histories and creates a merge commit.

Force a merge commit for a feature branch:

```bash
git merge --no-ff feature/my-change
```

Abort a merge:

```bash
git merge --abort
```

## Rebasing

Rebase replays commits from one branch onto another base:

```bash
git switch feature/my-change
git rebase main
```

Continue, skip, or abort a rebase:

```bash
git rebase --continue
git rebase --skip
git rebase --abort
```

Interactive rebase:

```bash
git rebase -i HEAD~3
```

This can squash, reword, reorder, edit, or drop local commits.

Rebasing rewrites commit hashes. Do not rebase commits that other people have already based work on unless the team agrees. If you must update a shared branch, prefer coordination and `git push --force-with-lease` over an unconditional force push.

## Resolve conflicts

A conflict occurs when Git cannot automatically combine changes. Conflicted files contain markers:

```text
<<<<<<< HEAD
current branch version
=======
incoming branch version
>>>>>>> feature/my-change
```

Resolution workflow:

1. Open each conflicted file and keep the correct combination of changes.
2. Remove all conflict markers.
3. Test the result.
4. Stage the resolved files.
5. Continue the merge or rebase.

```bash
git status
git add resolved-file.txt
git commit
# During a rebase:
git rebase --continue
```

To abandon the operation:

```bash
git merge --abort
git rebase --abort
```

Configure a merge tool if needed:

```bash
git config --global merge.tool vimdiff
git mergetool
```

## Ignore files

Create a `.gitignore` in the repository root:

```gitignore
*.log
.env
.venv/
node_modules/
build/
dist/
__pycache__/
```

Check why a path is ignored:

```bash
git check-ignore -v path/to/file
```

`.gitignore` only affects untracked files. Use `git rm --cached` to stop tracking a file that was already committed.

## Line endings and cross-platform work

Windows and Unix systems use different line endings. Configure a consistent policy:

```bash
# Linux/macOS
git config --global core.autocrlf input

# Windows
git config --global core.autocrlf true
```

For repository-specific control, add a `.gitattributes` file:

```gitattributes
* text=auto
*.sh text eol=lf
*.bat text eol=crlf
*.png binary
```

Avoid mixing line-ending changes with functional changes in the same commit; they make reviews noisy.

## Collaboration with GitHub, GitLab, and similar platforms

A typical hosted workflow:

1. Create an empty repository in the hosting service.
2. Add it as a remote.
3. Push the initial branch.
4. Protect the main branch and require reviews and checks.
5. Work on short-lived feature branches.
6. Open a pull request or merge request.
7. Run CI, review the diff, and merge.
8. Tag releases.

Example:

```bash
git remote add origin https://github.com/example-org/example-repo.git
git push -u origin main
git switch -c feature/my-change
# edit and commit
git push -u origin feature/my-change
```

### Fork workflow

When you do not have write access to the original repository:

```bash
git clone https://github.com/your-user/example-repo.git
cd example-repo
git remote add upstream https://github.com/example-org/example-repo.git
```

Synchronize your fork:

```bash
git fetch upstream
git switch main
git merge --ff-only upstream/main
git push origin main
```

Create a branch for your change, push it to your fork, and open a pull request against the upstream repository.

Do not commit passwords, tokens, private keys, customer data, or other secrets. Use environment variables, secret managers, or local untracked configuration files.

## Self-hosted Git lab over SSH

The following is a minimal lab example. It uses a shared `git` account and is not a production access-control design.

On the server:

```bash
sudo apt update
sudo apt install -y git
sudo useradd -m -s /bin/bash git
sudo passwd git
sudo mkdir -p /srv/git
sudo chown git:git /srv/git
```

On the client, create and copy an SSH key:

```bash
ssh-keygen -t ed25519 -C "you@example.test"
ssh-copy-id git@192.0.2.50
ssh git@192.0.2.50
```

Create a bare repository on the server:

```bash
sudo -u git git init --bare /srv/git/example-project.git
```

From a local project:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin git@192.0.2.50:/srv/git/example-project.git
git push -u origin main
```

Clone it elsewhere:

```bash
git clone git@192.0.2.50:/srv/git/example-project.git
```

For production, use a managed Git service or a properly access-controlled Git server. Define backup, patching, authentication, authorization, and audit requirements before hosting source code yourself.

## Best practices

- Commit small, focused changes with clear messages.
- Pull or fetch often and resolve drift early.
- Use one branch per feature, fix, or experiment.
- Review diffs before staging and before committing.
- Protect the main branch and require review and CI checks.
- Never commit secrets; add local secrets to `.gitignore`.
- Use annotated tags for releases and keep published tags immutable.
- Avoid rewriting shared history. Use `--force-with-lease` only when necessary.
- Use `git restore` for modern undo operations and `git revert` for shared history.
- Add CI checks for tests, linting, dependency scanning, and secret scanning.
- Back up or mirror critical repositories and test restoration.
- Document the team's merge, rebase, release, and hotfix conventions.

## Quick reference

| Task | Command |
| --- | --- |
| Show status | `git status -sb` |
| Show unstaged diff | `git diff` |
| Show staged diff | `git diff --staged` |
| Stage a file | `git add file.txt` |
| Stage selected hunks | `git add -p` |
| Commit | `git commit -m "Message"` |
| Amend last commit | `git commit --amend --no-edit` |
| Show history graph | `git log --oneline --graph --decorate --all` |
| Create and switch branch | `git switch -c feature/name` |
| Switch branch | `git switch main` |
| Merge branch | `git merge feature/name` |
| Rebase onto main | `git rebase main` |
| Fetch remote updates | `git fetch --prune` |
| Pull with rebase | `git pull --rebase` |
| Push branch | `git push -u origin feature/name` |
| Stash changes | `git stash push -m "Message"` |
| Restore stash | `git stash pop` |
| Unstage file | `git restore --staged file.txt` |
| Discard file changes | `git restore file.txt` |
| Revert commit | `git revert <commit>` |
| Create release tag | `git tag -a v1.0.0 -m "Release 1.0.0"` |
| Push tag | `git push origin v1.0.0` |
| Show remotes | `git remote -v` |
| Delete merged branch | `git branch -d feature/name` |
| Delete remote branch | `git push origin --delete feature/name` |

## Further reading

- [Git documentation](https://git-scm.com/doc)
- [Pro Git book](https://git-scm.com/book/en/v2)
- [GitHub Docs](https://docs.github.com)
- [GitLab Docs](https://docs.gitlab.com)
