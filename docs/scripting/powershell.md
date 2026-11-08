# PowerShell

PowerShell is a command shell and scripting language used for Windows administration and available on Linux and macOS. It passes structured .NET objects through the pipeline, rather than only plain text.

## Getting started

```powershell
$serviceName = "Spooler"
$service = Get-Service -Name $serviceName
$service | Select-Object Name, Status, StartType

Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name, CPU
```

Use `Get-Command` to discover commands, `Get-Help Get-Service -Examples` to read examples, and `Get-Member` to inspect the properties and methods on an object.

## Variables, pipelines, and conditions

```powershell
$servers = @("web-01", "web-02", "db-01")

foreach ($server in $servers) {
    if ($server -like "web-*") {
        Write-Output "Web server: $server"
    }
}
```

The pipeline passes objects from one command to another. Prefer filtering objects with `Where-Object` and selecting fields with `Select-Object` rather than parsing formatted screen output.

## Functions and error handling

```powershell
function Test-Endpoint {
    param(
        [Parameter(Mandatory)]
        [uri] $Uri
    )

    try {
        Invoke-RestMethod -Uri $Uri -TimeoutSec 10 -ErrorAction Stop
    }
    catch {
        Write-Error "Endpoint check failed: $($_.Exception.Message)"
        throw
    }
}
```

Use `-ErrorAction Stop` when a command's non-terminating error should enter `catch`. Re-throw failures that the caller must know about; avoid reporting success after an operation failed.

## Files, CSV, and JSON

```powershell
$servers = Import-Csv ./servers.csv
$servers | Where-Object Environment -eq "prod" |
    Export-Csv ./production-servers.csv -NoTypeInformation

$settings = Get-Content ./settings.json -Raw | ConvertFrom-Json
$settings | ConvertTo-Json -Depth 8 | Set-Content ./settings-copy.json
```

## Safe automation habits

- Use `-WhatIf` and `-Confirm` for commands that support them.
- Start with read-only queries and narrow the target scope.
- Keep credentials in an approved secret store or protected credential mechanism.
- Use explicit timeouts and handle API failures.
- Test in a development environment and verify the result.

## Practice project

Create a read-only server inventory report that collects service state, filters unhealthy services, exports CSV, and writes an error log. Add a `-WhatIf` mode before adding any remediation.

## Further reading

- [PowerShell documentation](https://learn.microsoft.com/powershell/)
- [PowerShell scripting documentation](https://learn.microsoft.com/powershell/scripting/overview)
