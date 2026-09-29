# GitHub workflows

## Repository connection and automatic deploys

Connect a GitHub repository from the app's Deploy surface, select the branch,
and choose whether successful branch updates deploy automatically. Required
checks should remain the gate when enabled; do not bypass them to make a failed
change deploy.
The connection, pipeline promotions, and review-app settings are customer
dashboard operations. CLI/MCP-only clients should prepare repository changes and
report the required dashboard step; MCP can verify build/release state afterwards.

Before diagnosing an automatic deploy, identify:

- repository and branch;
- commit SHA;
- whether automatic deploy is enabled;
- required-check state for that exact SHA;
- Watasu build and release IDs, if created.

Do not assume a successful GitHub workflow means Watasu created or released a
build. Correlate the same commit through both systems.

## Pipelines

A pipeline orders apps into stages. Promotion reuses the already-built artifact
instead of rebuilding from source. This makes the image identity the invariant
between stages while each app retains its own config, formation, add-ons, access,
and domains.

Before promotion, establish source app/release and destination stage. Treat a
production promotion as a deployment mutation and obtain the user's intent.

## Review apps

Review apps create an isolated app for a pull request and remove it when the
review lifecycle ends. Commit an `app.json` to describe the review environment.
Use `environments.review` for review-specific overrides.
Review apps require `app.json`. Parent process sizes are inherited with replica
counts capped at one before review formation overrides are applied. Review apps
and their managed resources are torn down when the PR closes or becomes draft;
keep production data and credentials out of review environments.

Example shape:

```json
{
  "env": {
    "APP_MODE": "review"
  },
  "addons": [
    { "plan": "postgresql:<current-plan>", "as": "DATABASE" }
  ],
  "formation": {
    "web": { "quantity": 1, "size": "<current-size>" }
  },
  "scripts": {
    "postdeploy": "bin/seed-review"
  },
  "environments": {
    "review": {
      "env": { "REVIEW_APP": "true" }
    }
  }
}
```

The placeholders are intentional: select current plan/size identifiers from the
docs or dashboard. Never commit a real credential. Keep seed/setup scripts
repeatable and scoped to the review app.

## GitHub Actions using the CLI

For custom automation:

- install a current Watasu CLI;
- store its API credential in GitHub Actions secrets;
- use explicit `--app <name>` and non-interactive flags;
- never print credentials or config values;
- preserve the same exact-SHA gates used for human-triggered deploys.

Prefer Watasu's repository connection for ordinary branch deployments. Use a
custom workflow when the repository needs orchestration beyond the product's
built-in connection.
