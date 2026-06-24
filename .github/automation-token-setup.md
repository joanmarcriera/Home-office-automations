# Automation token setup (`AUTOMATION_PAT`)

## Why
PRs opened with the default `GITHUB_TOKEN` do **not** trigger `on: pull_request`
workflows — a deliberate GitHub guard against recursive runs. That leaves the
shared `automation/weekly-rollup` PR's checks stuck in **`action_required`**, so
they never report and the PR can't merge on checks alone.

The three PR-creating workflows (`weekly-planner.yml`, `daily-digest.yml`,
`monthly-reddit-openclaw-intake.yml`) now open their PR with a real-identity
token:

```yaml
token: ${{ secrets.AUTOMATION_PAT || secrets.GITHUB_TOKEN }}
```

- **Secret present** → the PR is authored by that identity, so check workflows
  run automatically and the PR can auto-merge.
- **Secret absent** → falls back to `GITHUB_TOKEN` (today's behaviour: an inert
  PR whose checks are dispatched manually by the "Trigger PR gate workflows"
  step and re-run by `weekly-automation-rollup-merge.yml`). Nothing breaks.

## Option A — fine-grained PAT (simplest, recommended for a solo repo)
1. GitHub → **Settings → Developer settings → Fine-grained personal access
   tokens → Generate new token**.
2. **Resource owner:** your account. **Repository access:** *Only select
   repositories* → `Home-office-automations`.
3. **Repository permissions:** `Contents` = Read and write, `Pull requests` =
   Read and write, `Issues` = Read and write, `Workflows` = Read and write.
4. Set an expiry you're comfortable with (e.g. 1 year) and **Generate**. Copy
   the token (`github_pat_…`).
5. Add it as a repo secret:
   ```bash
   gh secret set AUTOMATION_PAT --repo joanmarcriera/Home-office-automations
   # paste the token when prompted
   ```
   (or GitHub → repo **Settings → Secrets and variables → Actions → New
   repository secret**, name `AUTOMATION_PAT`).

> Note: a fine-grained PAT expires. Set a calendar reminder to rotate it, or use
> Option B for a non-expiring, identity-independent setup.

## Option B — GitHub App token (more durable, no personal expiry)
1. Create a GitHub App (Settings → Developer settings → GitHub Apps) with
   **Contents: R/W, Pull requests: R/W, Issues: R/W, Workflows: R/W**; install
   it on this repo.
2. Store its **App ID** and **private key** as secrets `APP_ID` /
   `APP_PRIVATE_KEY`.
3. Mint a token per run and pass it as `AUTOMATION_PAT`:
   ```yaml
   - uses: actions/create-github-app-token@v1
     id: app-token
     with:
       app-id: ${{ secrets.APP_ID }}
       private-key: ${{ secrets.APP_PRIVATE_KEY }}
   # then use steps.app-token.outputs.token where AUTOMATION_PAT is referenced
   ```

## Verify
After adding the secret, manually run **Weekly Growth Planner** (Actions →
Run workflow). The refreshed `automation/weekly-rollup` PR should show its checks
**running automatically** instead of `action_required`.
