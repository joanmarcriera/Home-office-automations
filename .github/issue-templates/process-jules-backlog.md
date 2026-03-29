## Process Jules Backlog - @jules

This is an automated task to clear the backlog of open issues assigned to you. 

### Step 1 - Search for Open Issues
Search the repository for all open non-control issues that contain either the `jules` or `jules-blocked` label, excluding this exact issue.

### Step 2 - Address the Backlog
For each open issue found:
1. Read the issue description and any comments to understand the requested action.
2. If the issue has the `jules-blocked` label, inspect the blocker comment first.
   - If the blocker is transient or the task is now actionable, remove `jules-blocked`, re-add `jules`, and continue.
   - If it is still blocked, leave a comment explaining why it remains blocked and keep `jules-blocked`.
3. Complete the requested coding task, bug fix, or documentation update for actionable issues.
4. If the task is successful:
    - Open a pull request containing the fix/update. Include `Fixes #[Issue Number]` in the PR description so the issue closes automatically when merged.
5. If you are blocked, lack context, or encounter an error:
    - Leave a comment on the original issue explaining the blocker and remove the `jules` label from that issue to prevent it from stalling future backlog runs.

### Step 3 - Close this Issue
Once you have iterated through all the open `jules` / `jules-blocked` issues and completed actions, relabeled retriable items, or commented on blocked items, close this "Process Jules Backlog" issue.
