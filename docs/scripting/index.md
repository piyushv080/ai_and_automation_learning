# Scripting

Scripting helps automate small, repeatable tasks and provides building blocks for larger infrastructure workflows. Pick a language based on the environment, available libraries, and the people who will maintain the script.

<div class="grid cards" markdown>

-   **Python**

    ---

    General-purpose scripting, APIs, data processing, and infrastructure integrations.

    [Python basics](../python-basics.md) · [Infrastructure automation](../python-infrastructure-automation.md)

-   **PowerShell**

    ---

    Windows administration, Microsoft services, and cross-platform command automation.

    [PowerShell notes](powershell.md)

-   **Bash and shell**

    ---

    Linux command-line workflows, file operations, and system administration.

    [Bash and shell notes](bash.md)

-   **JavaScript**

    ---

    Browser scripting, Node.js tools, and JSON-based APIs.

    [JavaScript notes](javascript.md)

</div>

## Choosing a language

| Language | A good fit for | First practice task |
| --- | --- | --- |
| Python | APIs, structured data, cross-platform automation | Read a JSON inventory and report unhealthy systems. |
| PowerShell | Windows systems and Microsoft administration | Collect service status and export a CSV report. |
| Bash | Linux command-line tasks and glue scripts | Check disk usage and produce a concise status report. |
| JavaScript | Web tasks, Node.js utilities, and API clients | Call a test endpoint and display the JSON result. |

Keep scripts small, validate their inputs, avoid embedding credentials, handle failures clearly, and test against non-production data first.
