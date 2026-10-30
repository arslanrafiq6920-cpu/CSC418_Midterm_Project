# Assignment Submission Portal — CSC418 DevOps Midterm

## Requirements
- Python 3.10 or newer
- Git
- GitHub account
- For local report delivery from GitHub-hosted CI: a publicly reachable HTTPS tunnel to your local receiver

## 1. Run the portal
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

Submissions are held in memory for this demo and reset when the app restarts.

## 2. Run automated tests
```bash
pytest -v
```
The three tests cover a valid submission, a missing registration number, and an invalid URL.

## 3. Start the local report receiver
In a second terminal:
```bash
# Windows PowerShell:
$env:REPORT_TOKEN="replace-with-a-long-random-secret"
python receiver.py
```
Linux/macOS:
```bash
export REPORT_TOKEN="replace-with-a-long-random-secret"
python receiver.py
```
The receiver listens on port 8000 and writes `test-report.json` in the current project folder whenever it receives a valid report.

## 4. Connect GitHub Actions to your computer
A GitHub-hosted runner's `localhost` is not your computer. Keep the receiver running and expose port 8000 using a trusted HTTPS tunnel service (for example, a temporary Cloudflare Tunnel or ngrok URL). Do not publish the token or commit it to GitHub.

In GitHub, open **Repository → Settings → Secrets and variables → Actions → New repository secret** and add:
- `LOCAL_RECEIVER_URL`: the tunnel's HTTPS base URL, without `/report` (example shape: `https://your-subdomain.example`)
- `REPORT_TOKEN`: the same secret used by `receiver.py`

Keep the tunnel and receiver running while the workflow executes. Test `/health` through the tunnel before pushing. The report receiver overwrites `test-report.json` on each report.

## 5. Push the project to GitHub
Create an empty repository named `CSC418-Midterm` on GitHub. From this folder run:
```bash
git init
git add .
git commit -m "Build assignment submission portal and CI tests"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/CSC418-Midterm.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username. Open the repository's **Actions** tab to see the workflow.

## 6. Demonstrate passing, failing, then fixed
1. Push the working version. Show the three tests passing and the local `test-report.json`.
2. In `app.py`, temporarily break URL validation by changing `return parsed.scheme in ("http", "https") and bool(parsed.netloc)` to `return True`.
3. Commit and push the defect. The invalid-URL test should fail, and the workflow should be red. The receiver should automatically overwrite `test-report.json` with the failing run's results.
4. Restore the original URL validation line, commit, and push. The workflow should turn green and the JSON report should show all tests passing again.

Do not leave the intentional defect in your final submission.

## Report fields
The JSON report contains repository name, branch, commit SHA, workflow run ID, UTC timestamp, individual test names/results/failure messages, total/passed/failed counts, and overall status.
