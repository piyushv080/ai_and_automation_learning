# Application Security and Observability

Study notes on application security scanning, software dependencies, monitoring, and service-level measurements. Tool behavior and configuration vary by product and version.

## Static and dynamic application security testing

- **Static Application Security Testing (SAST)** analyzes source code or compiled artifacts without running the application. It can find insecure patterns early in development, though findings need review for context and false positives.
- **Dynamic Application Security Testing (DAST)** tests a running application from the outside. It can identify issues visible during execution, but requires a suitable test environment and safe test data.

These methods are complementary. Use approved environments and follow the organization's process for triage, remediation, and exceptions.

## Code and dependency scanning

### Static analysis rules

Static analysis tools such as Fortify apply rules to identify possible security weaknesses, code quality problems, or policy violations. Rule sets can be configured to match an organization's standards. Review the finding, affected code path, severity, and remediation guidance before deciding how to fix or disposition it.

### Open-source dependency scanning

Software composition analysis tools such as Black Duck inspect open-source dependencies for known vulnerabilities, license obligations, and policy violations. A useful response checks the dependency and version, whether the affected code is reachable, available fixed versions, and compatibility before upgrading or requesting an exception.

## Monitoring and dashboards

Monitoring agents and instrumentation can collect application performance data, traces, logs, and infrastructure metrics for analysis in platforms such as New Relic. OpenTelemetry is another commonly used instrumentation standard. Protect telemetry: it can contain personal or confidential data if applications include sensitive values in attributes or logs.

Dashboards in tools such as New Relic and Grafana should answer a specific operational question. Prefer a small set of actionable signals, clear units and time ranges, service ownership, and links to relevant logs or runbooks. A dashboard is not a substitute for alert thresholds and an incident response process.

For a hands-on metrics lab, see the [Prometheus and Grafana guide](prometheus-grafana-guide.md).

## SLI, SLO, and SLA

- **Service Level Indicator (SLI):** a measured value describing service behavior, such as request success rate or latency.
- **Service Level Objective (SLO):** a target for an SLI over a defined period, such as 99.9% successful requests over 30 days.
- **Service Level Agreement (SLA):** a formal commitment between a provider and a customer, often with remedies if agreed service levels are not met.

An SLO should be based on a meaningful user-facing SLI and a clear measurement window. Teams can use the difference between the SLO target and observed reliability to manage an error budget.

## Practical response to a finding or alert

1. Confirm the affected application, version, environment, and time range.
2. Review the scanner evidence or monitoring signal; check for false positives and missing context.
3. Assess severity, user impact, exposure, and available mitigations.
4. Assign an owner, remediation action, and due date according to policy.
5. Verify the fix or recovery with a rescan or independent health check.
6. Record the result and update runbooks, dashboards, or tests where useful.

## Further reading

- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
- [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [Grafana documentation](https://grafana.com/docs/)
