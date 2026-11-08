# AI and Automation Learning

A static learning catalog built from Markdown with Zensical and published on GitHub Pages. Learning areas include scripting, cloud infrastructure, automation technologies, DevOps engineering, projects, and documentation. Add topic pages under `docs/` and include them in `mkdocs.yml` navigation.

## Preview locally

From this folder (the repository root), create and activate a virtual environment.

### Linux / WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
zensical serve
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
zensical serve
```

Open the local URL printed by Zensical (usually `http://127.0.0.1:8000`).

If you move or rename this repository after creating `.venv`, recreate the environment because virtual environments store their original path. On Linux/WSL, run `deactivate` if needed, then `python3 -m venv --clear .venv`, `source .venv/bin/activate`, and reinstall the requirements.

## Publish on GitHub Pages

The workflow is in `.github/workflows/pages.yml`. Push to `dev`, `main`, or `master` to build and publish this site, or start it manually from the **Actions** tab. In the GitHub repository, open **Settings → Pages** and set **Build and deployment → Source** to **GitHub Actions**.

The workflow publishes the website at the repository's GitHub Pages URL. The sample pages are in `docs/`; add Markdown files there and include them in the navigation in `mkdocs.yml`.
