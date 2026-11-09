# Cloud Infrastructure

Cloud infrastructure provides on-demand compute, networking, storage, identity, and managed services. The same operating principles apply across AWS, Azure, Google Cloud, and private cloud platforms.

## Core building blocks

| Area | Questions to understand |
| --- | --- |
| Identity and access | Who or what can access a resource? What is the least privilege required? |
| Compute | Should the workload run on a VM, container, function, or managed platform? |
| Networking | How are subnets, routes, DNS, load balancers, and firewalls arranged? |
| Storage | What data is stored, how is it protected, and how long is it retained? |
| Operations | How are health, logs, metrics, patching, backup, and recovery handled? |
| Cost and governance | Who owns the resource, what does it cost, and what policies apply? |

## A practical learning sequence

1. Review [Linux foundations](linux-notes.md) and [networking foundations](networking-notes.md).
2. Learn identity, regions/zones, virtual networks, compute, and storage in one cloud provider.
3. Deploy a small non-production workload with monitoring and a clear teardown plan.
4. Rebuild it using infrastructure as code and source control.
5. Add automation, security checks, cost awareness, backup, and documented recovery steps.

## Cloud design habits

- Prefer identity roles and short-lived credentials over long-lived access keys.
- Make network exposure explicit and restrict management paths.
- Tag resources with owner, environment, and purpose.
- Use repeatable deployments and review plans before applying changes.
- Configure budgets, logging, monitoring, backups, and deletion policies early.
- Test recovery and verify actual service health after deployment.

## Project idea

Deploy a small static website or test service in a sandbox account. Document its network path, identity permissions, monitoring, estimated cost, and teardown steps. Keep credentials out of source control and remove resources when finished.
