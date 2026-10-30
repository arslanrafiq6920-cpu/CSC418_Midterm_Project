"""Convert pytest-json-report output into the required portable report."""
import json, os
from datetime import datetime, timezone
from pathlib import Path

source = Path("pytest-report.json")
try:
    raw = json.loads(source.read_text(encoding="utf-8"))
except (FileNotFoundError, json.JSONDecodeError):
    raw = {}

tests = []
for item in raw.get("tests", []):
    outcome = item.get("outcome", "unknown")
    call = item.get("call", {}) or {}
    longrepr = call.get("longrepr") or item.get("setup", {}).get("longrepr") or item.get("teardown", {}).get("longrepr")
    tests.append({
        "name": item.get("nodeid", "unknown"),
        "result": "passed" if outcome == "passed" else ("failed" if outcome == "failed" else outcome),
        "failure_message": str(longrepr) if outcome == "failed" and longrepr else None
    })

summary_raw = raw.get("summary", {}) or {}
total = summary_raw.get("total", len(tests))
passed = summary_raw.get("passed", sum(t["result"] == "passed" for t in tests))
failed = summary_raw.get("failed", sum(t["result"] == "failed" for t in tests))
# Include a setup/collection error if pytest failed but no individual test result exists.
exit_code = int(os.environ.get("PYTEST_EXIT_CODE", "1"))
status = "passed" if exit_code == 0 and failed == 0 else "failed"

report = {
    "repository_name": os.environ.get("GITHUB_REPOSITORY", "local-run"),
    "branch": os.environ.get("GITHUB_REF_NAME", "local"),
    "commit_sha": os.environ.get("GITHUB_SHA", "local"),
    "pipeline_run_identifier": os.environ.get("GITHUB_RUN_ID", "local"),
    "execution_timestamp": datetime.now(timezone.utc).isoformat(),
    "tests": tests,
    "summary": {"total": total, "passed": passed, "failed": failed, "status": status},
}
Path("test-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report["summary"], indent=2))
