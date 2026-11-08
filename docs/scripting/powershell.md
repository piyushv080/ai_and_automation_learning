# PowerShell

PowerShell is a command shell and scripting language used for Windows administration and available on Linux and macOS. It passes structured .NET objects through the pipeline, which makes it useful for inventory, system health, and report automation.

This guide uses generic, read-only examples based on common learning-lab exercises: querying services and processes, collecting system information, working with CSV/JSON/XML, handling errors, and producing reports. Remote commands are shown only as patterns; use them only on systems you are authorized to manage.

## 1. Discover commands and objects

```powershell
Get-Command *Process*             # discover commands by name
Get-Help Get-Process -Examples    # read examples
Get-Service | Get-Member          # inspect object properties and methods
Get-Service | Select-Object -First 5 Name, Status
```

PowerShell commands generally use the `Verb-Noun` pattern. Use `Get-Command`, `Get-Help`, and `Get-Member` before guessing a command or property name.

The pipeline passes objects between commands. Filter and select objects before formatting them. `Format-Table` and `Format-List` are for the final display step; do not send formatted output to later commands that expect objects.

```powershell
Get-Process |
    Where-Object { $_.CPU -gt 0 } |
    Sort-Object CPU -Descending |
    Select-Object -First 10 ProcessName, Id, CPU
```

## 2. Variables, collections, and conditions

Variables start with `$`. Arrays hold ordered collections; hashtables hold named key-value pairs; custom objects are useful for structured report rows.

```powershell
$servers = @("localhost", "server-a.example.test")
$server = [pscustomobject]@{
    Name        = "web-01"
    Environment = "dev"
    Healthy     = $true
}

foreach ($name in $servers) {
    if ($name -eq "localhost") {
        Write-Output "Checking the local computer"
    }
}
```

Use `$null` comparisons with `$null` on the left (`$null -eq $value`). Use `-eq`, `-ne`, `-like`, and `-match` for comparisons and pattern matching.

## 3. Functions and parameters

Use parameters to make scripts reusable instead of editing hard-coded values. Add validation when an input has a defined range.

```powershell
function Get-HealthLabel {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateRange(0, 100)]
        [int] $UsedPercent
    )

    if ($UsedPercent -ge 90) {
        return "Critical"
    }
    if ($UsedPercent -ge 75) {
        return "Warning"
    }
    return "Healthy"
}

Get-HealthLabel -UsedPercent 62
```

Use `Write-Output` or `return` for values a caller should receive. Use `Write-Warning`, `Write-Verbose`, and `Write-Error` for messages with meaning; reserve `Write-Host` for display that should not be part of the pipeline.

## 4. Files and structured data

### Paths and text files

```powershell
$reportPath = Join-Path $HOME "reports\service-status.csv"
$reportDirectory = Split-Path -Parent $reportPath

New-Item -ItemType Directory -Path $reportDirectory -Force | Out-Null
Get-Content -Path ./settings.txt -ErrorAction Stop
```

Use `Join-Path` instead of manually joining path fragments. `-Force` makes directory creation repeatable, but review the destination before writing.

### CSV

CSV is useful for inventory input and reports. Convert objects to CSV rather than building comma-separated strings yourself.

```powershell
$services = Get-Service |
    Select-Object Name, Status, DisplayName

$services | Export-Csv -Path $reportPath -NoTypeInformation
$reviewRows = Import-Csv -Path $reportPath
$reviewRows | Where-Object Status -eq "Running" |
    Select-Object -First 10 Name, Status
```

### JSON and XML

```powershell
$settings = Get-Content -Path ./settings.json -Raw | ConvertFrom-Json
$settings | ConvertTo-Json -Depth 8 | Set-Content -Path ./settings-copy.json

[xml] $catalog = Get-Content -Path ./sample.xml -Raw
$catalog.SelectNodes("//item") | Select-Object name, id
```

Validate the schema and required fields before using parsed configuration to make changes.

## 5. Querying services, processes, and system information

These are read-only examples for the local machine:

```powershell
Get-Service |
    Select-Object Name, Status, StartType |
    Sort-Object Name

Get-Process |
    Sort-Object CPU -Descending |
    Select-Object -First 10 ProcessName, Id, CPU, WorkingSet64

Get-CimInstance -ClassName Win32_OperatingSystem |
    Select-Object CSName, Caption, LastBootUpTime,
        @{ Name = "FreeMemoryMB"; Expression = { [math]::Round($_.FreePhysicalMemory / 1024, 1) } }
```

`Get-CimInstance` queries Common Information Model (CIM) data and is the modern choice for many Windows management queries. The available classes and properties depend on the operating system.

### Querying approved remote computers

The `-ComputerName` parameter can query multiple computers when the environment supports the required remoting protocol and permissions. Start with a small, approved list and handle individual failures.

```powershell
$computerNames = @($env:COMPUTERNAME) # replace only with an approved test target

foreach ($computerName in $computerNames) {
    try {
        Get-CimInstance -ClassName Win32_OperatingSystem `
            -ComputerName $computerName -ErrorAction Stop |
            Select-Object CSName, Caption, LastBootUpTime
    }
    catch {
        Write-Warning "Could not query $computerName ($($_.Exception.GetType().Name))"
    }
}
```

Avoid storing production host lists, credentials, or domain details in a public learning page. Use the organization's approved inventory and authentication methods in real work.

## 6. Error handling

PowerShell has terminating and non-terminating errors. `-ErrorAction Stop` promotes a command error so `catch` can handle it.

```powershell
try {
    $service = Get-Service -Name "Spooler" -ErrorAction Stop
    [pscustomobject]@{
        Name   = $service.Name
        Status = $service.Status
    }
}
catch {
    Write-Error "Service query failed: $($_.Exception.Message)"
    throw
}
finally {
    Write-Verbose "Service query finished"
}
```

Catch only errors you can handle. Preserve failure status when the operation did not succeed; do not silently convert failures into success.

## 7. Generate a simple health report

This example collects local, read-only operating-system and service information, then exports it to CSV and HTML.

```powershell
$os = Get-CimInstance -ClassName Win32_OperatingSystem
$report = [pscustomobject]@{
    ComputerName = $os.CSName
    OperatingSystem = $os.Caption
    LastBoot = $os.LastBootUpTime
    RunningServices = (Get-Service | Where-Object Status -eq "Running").Count
    CollectedAt = Get-Date
}

$outputDirectory = Join-Path $HOME "reports"
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

$report | Export-Csv -Path (Join-Path $outputDirectory "system-health.csv") -NoTypeInformation
$report | ConvertTo-Html -Title "System Health Summary" |
    Set-Content -Path (Join-Path $outputDirectory "system-health.html")
```

Reports may contain host and software details. Keep sample reports local and review fields before sharing or publishing.

## 8. Remoting and safe change patterns

PowerShell remoting can run commands on other systems when WinRM or another supported transport is configured. Learn read-only queries first. For change operations, restrict the target list, require appropriate authorization, use `SupportsShouldProcess`/`-WhatIf` where supported, and verify the final state.

Do not weaken execution policy globally just to run a script. Use signed or reviewed scripts and follow the system's approved execution policy.

## 9. Practice projects

1. Export local service status to CSV and filter stopped services.
2. Query local operating-system details with CIM and calculate available memory in MB.
3. Create a top-process report with `Get-Process`, `Sort-Object`, and `Select-Object`.
4. Import sample XML and JSON, then validate required fields.
5. Add error handling for a missing input file and a failed CIM query.
6. Extend a read-only report to approved remote test computers and record per-host failures.

## Further reading

- [PowerShell documentation](https://learn.microsoft.com/powershell/)
- [PowerShell scripting documentation](https://learn.microsoft.com/powershell/scripting/overview)
- [Get-CimInstance reference](https://learn.microsoft.com/powershell/module/cimcmdlets/get-ciminstance)
