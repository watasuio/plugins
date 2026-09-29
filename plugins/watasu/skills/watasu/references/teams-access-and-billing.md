# Teams, access, and billing

## Ownership

Teams own apps, add-ons, sandboxes, and billing. Resolve the team before creating
a billable resource. Do not assume that organization membership grants access to
every app.

## Access model

Team roles establish team-wide administration/membership. App and pipeline roles
grant scoped capabilities:

- Admin: team administration and access to team apps.
- Billing: financial access without app or operational access.
- Member: team membership without automatic access to existing apps.

Inspect with `watasu members --team <team>` and `watasu access --app <app>`.
After an authorized grant, use `watasu members add <email> --role <role> --team
<team>` for membership and `watasu access add <email> --permissions view,deploy
--app <app>` for scoped app access. Confirm command-specific help for updates
and removals. Membership and app access are separate grants.

| Role | Typical capability |
| --- | --- |
| Viewer | Inspect app state |
| Deployer | Push code and trigger builds |
| Operator | Operate formation/runtime resources |
| Maintainer | Manage app settings and access |

Permissions are additive when a user receives access from more than one path.
Use the current access page for the precise permission matrix.

For sensitive apps:

- lock self-join or broad inherited access;
- grant the narrowest role that supports the task;
- review pipeline access as well as direct app access;
- remove access intentionally rather than assuming a team-role change removes
  every grant.

Any change to collaborators, team membership, role, self-join, or production
access is a mutation and requires the user's intent.

Use `apps:join`/`apps:leave` for the current user's app membership and
`apps:lock`/`apps:unlock` for self-join policy, always with `--app`. Pipeline access
and invitations are managed in the customer dashboard. Notifications follow the
recipient's access and notification preferences; a Viewer should not be assumed
to receive deploy-failure notifications.

## Plans and billing

Billing can include app process usage, dynamic pod usage, managed add-ons,
sandbox runtime/storage, templates, checkpoints, volumes, and data transfer.
Plan names, included quotas, prices, and limits change over time. Consult the
live dashboard and current docs before quoting or comparing them.

Billing is prepaid. Check the selected team's balance, charges, and subscription
in the dashboard; MCP does not expose billing. Suspension can block deployments
and sandbox work. Use the customer's top-up flow to resolve a balance issue,
never an administrator credit or backend-console procedure. Payment, automatic
top-up, plan changes, and account deletion require explicit user intent.

Durable guidance:

- creating an app alone is not the same as running paid formation;
- add-ons and sandbox resources can remain billable independently;
- paused sandbox behavior and retained disk/storage are different billing
  dimensions;
- checkpoints, volumes, and template artifacts can outlive a running sandbox;
- Dynamic app sizes bill measured CPU/memory within selected ceilings; replica
  count stays explicit and this is not synonymous with scale-to-zero.

When investigating an unexpected charge, enumerate resources by team and period,
including detached or retained sandbox storage. Do not delete anything merely to
reduce cost without explicit confirmation.
