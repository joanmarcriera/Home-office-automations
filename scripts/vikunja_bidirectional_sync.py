#!/usr/bin/env python3
"""
Bidirectional sync between GitHub Issues and Vikunja tasks.

Environment:
  GH_TOKEN                     (required)
  GITHUB_REPOSITORY            (required, owner/repo)
  VIKUNJA_BASE_URL             (required, e.g. https://vikunja.example.com)
  VIKUNJA_API_TOKEN            (required)
  VIKUNJA_PROJECT_ID           (required, integer)
  VIKUNJA_SYNC_LABEL           (optional, default: sync-vikunja)
  VIKUNJA_SYNC_LIMIT           (optional, default: 200)
  VIKUNJA_IMPORT_UNLINKED_TASKS(optional, default: false)
  VIKUNJA_SYNC_DRY_RUN         (optional, default: false)
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

GH_API_BASE = "https://api.github.com"
GH_TASK_MARKER_RE = re.compile(r"<!--\s*vikunja-task-id:(\d+)\s*-->")
VK_ISSUE_MARKER_RE = re.compile(r"<!--\s*github-issue:([^#]+/[^#]+)#(\d+)\s*-->")


def env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


class HttpClient:
    def __init__(self, base_url: str, headers: dict[str, str]):
        self.base_url = base_url.rstrip("/")
        self.headers = headers

    def request(self, method: str, path: str, payload: dict | list | None = None) -> Any:
        url = f"{self.base_url}{path}"
        data = None
        req_headers = dict(self.headers)
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            req_headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url=url, data=data, headers=req_headers, method=method.upper())
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            if not body:
                return {}
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {"raw": body}


def gh_path(repo: str, suffix: str) -> str:
    return f"/repos/{repo}{suffix}"


def get_task_marker(issue_body: str | None) -> int | None:
    if not issue_body:
        return None
    match = GH_TASK_MARKER_RE.search(issue_body)
    if not match:
        return None
    return int(match.group(1))


def get_issue_marker(task_desc: str | None) -> tuple[str, int] | None:
    if not task_desc:
        return None
    match = VK_ISSUE_MARKER_RE.search(task_desc)
    if not match:
        return None
    return match.group(1), int(match.group(2))


def marker_for_issue(repo: str, issue_number: int) -> str:
    return f"<!-- github-issue:{repo}#{issue_number} -->"


def marker_for_task(task_id: int) -> str:
    return f"<!-- vikunja-task-id:{task_id} -->"


def task_done(task: dict) -> bool:
    return bool(task.get("done", False))


def format_task_title(issue_number: int, title: str) -> str:
    return f"GH #{issue_number}: {title}".strip()[:240]


def build_task_description(repo: str, issue: dict) -> str:
    body = (issue.get("body") or "").strip()
    marker = marker_for_issue(repo, issue["number"])
    if marker in body:
        return body
    if body:
        return f"{body}\n\n{marker}\n"
    return f"{marker}\n"


def build_issue_body_from_task(repo: str, task: dict) -> str:
    task_id = task.get("id")
    task_title = task.get("title", "(untitled)")
    task_desc = (task.get("description") or "").strip()
    marker = marker_for_task(int(task_id))
    lines = [
        f"Synced from Vikunja task `{task_id}`.",
        "",
        f"Task title: {task_title}",
        "",
    ]
    if task_desc:
        lines.extend(["Task description:", task_desc, ""])
    lines.append(marker)
    return "\n".join(lines)


def normalize_vikunja_base(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/api/v1"):
        return base
    return f"{base}/api/v1"


def extract_task_list(data: Any) -> tuple[list[dict], bool]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)], True
    if isinstance(data, dict):
        if isinstance(data.get("tasks"), list):
            return [x for x in data["tasks"] if isinstance(x, dict)], True
        if isinstance(data.get("data"), list):
            return [x for x in data["data"] if isinstance(x, dict)], True
    return [], False


def list_vikunja_tasks(vk: HttpClient, project_id: int, limit: int) -> list[dict]:
    endpoints = [
        f"/projects/{project_id}/tasks?page=1&per_page={limit}",
        f"/projects/{project_id}/tasks",
        f"/tasks?project_id={project_id}&page=1&per_page={limit}",
        f"/tasks/all?project_id={project_id}&page=1&per_page={limit}",
    ]
    errors: list[str] = []
    for endpoint in endpoints:
        try:
            data = vk.request("GET", endpoint)
            tasks, recognized = extract_task_list(data)
            if recognized:
                return tasks[:limit]
        except urllib.error.HTTPError as exc:
            errors.append(f"{endpoint}: HTTP {exc.code}")
        except Exception as exc:  # pragma: no cover - defensive
            errors.append(f"{endpoint}: {exc}")
    raise RuntimeError("Could not list Vikunja tasks. Tried endpoints: " + "; ".join(errors))


def create_vikunja_task(vk: HttpClient, project_id: int, payload: dict) -> dict:
    payload_with_project = dict(payload)
    payload_with_project["project_id"] = project_id
    endpoints = [
        ("/projects/{}/tasks".format(project_id), payload),
        ("/tasks", payload_with_project),
    ]
    last_error: str = ""
    for endpoint, body in endpoints:
        try:
            data = vk.request("PUT", endpoint, body)
            if isinstance(data, dict) and data:
                return data
        except urllib.error.HTTPError as exc:
            last_error = f"{endpoint}: HTTP {exc.code}"
        except Exception as exc:  # pragma: no cover - defensive
            last_error = f"{endpoint}: {exc}"
    raise RuntimeError(f"Failed to create Vikunja task ({last_error})")


def update_vikunja_task(vk: HttpClient, task_id: int, payload: dict) -> None:
    endpoints = [("POST", f"/tasks/{task_id}"), ("PUT", f"/tasks/{task_id}")]
    last_error: str = ""
    for method, endpoint in endpoints:
        try:
            vk.request(method, endpoint, payload)
            return
        except urllib.error.HTTPError as exc:
            last_error = f"{method} {endpoint}: HTTP {exc.code}"
        except Exception as exc:  # pragma: no cover - defensive
            last_error = f"{method} {endpoint}: {exc}"
    raise RuntimeError(f"Failed to update Vikunja task {task_id} ({last_error})")


def parse_task_id(created: dict) -> int:
    if isinstance(created.get("id"), int):
        return int(created["id"])
    if isinstance(created.get("task"), dict) and isinstance(created["task"].get("id"), int):
        return int(created["task"]["id"])
    raise RuntimeError("Could not parse Vikunja task id from create response.")


def ensure_sync_label(gh: HttpClient, repo: str, label: str, dry_run: bool) -> None:
    safe = urllib.parse.quote(label, safe="")
    try:
        gh.request("GET", gh_path(repo, f"/labels/{safe}"))
        return
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
    if dry_run:
        print(f"[dry-run] would create label `{label}`")
        return
    gh.request(
        "POST",
        gh_path(repo, "/labels"),
        {"name": label, "color": "0e8a16", "description": "Synced with Vikunja"},
    )


def main() -> int:
    repo = env("GITHUB_REPOSITORY")
    gh_token = env("GH_TOKEN")
    vk_base = normalize_vikunja_base(env("VIKUNJA_BASE_URL"))
    vk_token = env("VIKUNJA_API_TOKEN")
    project_id = int(env("VIKUNJA_PROJECT_ID"))
    sync_label = env("VIKUNJA_SYNC_LABEL", "sync-vikunja")
    limit = int(env("VIKUNJA_SYNC_LIMIT", "200"))
    import_unlinked = as_bool(os.getenv("VIKUNJA_IMPORT_UNLINKED_TASKS"), default=False)
    dry_run = as_bool(os.getenv("VIKUNJA_SYNC_DRY_RUN"), default=False)

    gh = HttpClient(
        GH_API_BASE,
        {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {gh_token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "home-office-vikunja-sync",
        },
    )
    vk = HttpClient(
        vk_base,
        {
            "Authorization": f"Bearer {vk_token}",
            "Accept": "application/json",
            "User-Agent": "home-office-vikunja-sync",
        },
    )

    ensure_sync_label(gh, repo, sync_label, dry_run)

    gh_issues = gh.request(
        "GET",
        gh_path(
            repo,
            f"/issues?state=all&sort=updated&direction=desc&per_page={limit}",
        ),
    )
    issues = []
    for issue in gh_issues:
        if "pull_request" in issue:
            continue
        labels = {x.get("name") for x in issue.get("labels", []) if isinstance(x, dict)}
        if sync_label and sync_label not in labels:
            continue
        issues.append(issue)

    tasks = list_vikunja_tasks(vk, project_id, limit)
    tasks_by_id = {int(t["id"]): t for t in tasks if isinstance(t.get("id"), int)}
    issue_by_number = {int(i["number"]): i for i in issues}

    print(f"Loaded {len(issues)} GitHub issue(s) and {len(tasks_by_id)} Vikunja task(s).")

    # GitHub -> Vikunja
    for issue in issues:
        issue_num = int(issue["number"])
        issue_state = issue.get("state", "open")
        linked_task_id = get_task_marker(issue.get("body"))
        payload = {
            "title": format_task_title(issue_num, issue.get("title", "(untitled)")),
            "description": build_task_description(repo, issue),
            "done": issue_state == "closed",
            "project_id": project_id,
        }

        if linked_task_id and linked_task_id in tasks_by_id:
            if dry_run:
                print(f"[dry-run] update task {linked_task_id} from issue #{issue_num}")
            else:
                update_vikunja_task(vk, linked_task_id, payload)
        elif linked_task_id and linked_task_id not in tasks_by_id:
            print(f"Issue #{issue_num} references missing task {linked_task_id}; creating replacement.")
            linked_task_id = None

        if not linked_task_id:
            if dry_run:
                print(f"[dry-run] create task for issue #{issue_num}")
                continue
            created = create_vikunja_task(vk, project_id, payload)
            new_task_id = parse_task_id(created)
            body = issue.get("body") or ""
            body = (body.rstrip() + "\n\n" + marker_for_task(new_task_id) + "\n").strip() + "\n"
            gh.request("PATCH", gh_path(repo, f"/issues/{issue_num}"), {"body": body})
            print(f"Linked issue #{issue_num} -> task {new_task_id}")

    # Vikunja -> GitHub
    for task in tasks_by_id.values():
        task_id = int(task["id"])
        marker = get_issue_marker(task.get("description"))
        if marker:
            marker_repo, issue_num = marker
            if marker_repo != repo:
                continue
            issue = issue_by_number.get(issue_num)
            if not issue:
                # Issue may be outside loaded window; skip safely.
                continue
            is_done = task_done(task)
            issue_state = issue.get("state")
            if is_done and issue_state != "closed":
                if dry_run:
                    print(f"[dry-run] close issue #{issue_num} from task {task_id}")
                else:
                    gh.request("PATCH", gh_path(repo, f"/issues/{issue_num}"), {"state": "closed"})
            if (not is_done) and issue_state == "closed":
                if dry_run:
                    print(f"[dry-run] reopen issue #{issue_num} from task {task_id}")
                else:
                    gh.request("PATCH", gh_path(repo, f"/issues/{issue_num}"), {"state": "open"})
            continue

        if task_done(task):
            continue
        if not import_unlinked:
            continue

        issue_title = f"[Vikunja] {task.get('title', '(untitled task)')}"[:240]
        issue_body = build_issue_body_from_task(repo, task)
        payload = {"title": issue_title, "body": issue_body, "labels": [sync_label]}
        if dry_run:
            print(f"[dry-run] create issue from unlinked task {task_id}")
            continue
        created_issue = gh.request("POST", gh_path(repo, "/issues"), payload)
        new_issue_num = int(created_issue["number"])
        description = (task.get("description") or "").strip()
        description = (description + "\n\n" + marker_for_issue(repo, new_issue_num)).strip() + "\n"
        update_vikunja_task(vk, task_id, {"description": description, "project_id": project_id})
        print(f"Linked task {task_id} -> issue #{new_issue_num}")

    print("Vikunja/GitHub sync complete.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - defensive
        print(f"Sync failed: {exc}")
        raise SystemExit(1)
