[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Init', 'Status', 'SetRoot', 'Capture', 'Query')]
    [string]$Action,

    [string]$MemoryRoot,

    [ValidateSet('Inbox', 'Task', 'Knowledge', 'All')]
    [string]$Type,

    [string]$Title,

    [string]$Content,

    [string]$TargetFile,

    [string]$Query,

    [ValidateSet('Active', 'Completed', 'All')]
    [string]$Status,

    [ValidateRange(1, 50)]
    [int]$Limit,

    [ValidateSet('True', 'False')]
    [string]$RequireObsidian,

    [ValidateSet('Auto', 'Manual')]
    [string]$ExperienceMode
)

$ErrorActionPreference = 'Stop'
$PythonScript = Join-Path $PSScriptRoot 'write-memory.py'

if (-not (Test-Path -LiteralPath $PythonScript -PathType Leaf)) {
    throw "缺少跨平台写入器：$PythonScript"
}

$PythonCommand = $null
$PythonPrefix = @()

foreach ($Candidate in @('python', 'py', 'python3')) {
    $Resolved = Get-Command $Candidate -ErrorAction SilentlyContinue
    if ($null -eq $Resolved) {
        continue
    }

    $CandidatePrefix = @()
    if ($Candidate -eq 'py') {
        $CandidatePrefix = @('-3')
    }

    & $Resolved.Source @CandidatePrefix -c `
        'import sys; raise SystemExit(sys.version_info < (3, 8))' *> $null
    if ($LASTEXITCODE -ne 0) {
        continue
    }

    $PythonCommand = $Resolved.Source
    $PythonPrefix = $CandidatePrefix
    break
}

if ($null -eq $PythonCommand) {
    throw '需要 Python 3.8 或更高版本，并确保 python3、python 或 py 已加入 PATH。'
}

$CliArgs = @(
    $PythonPrefix
    $PythonScript
    '--action'
    $Action.ToLowerInvariant()
)

if (-not [string]::IsNullOrWhiteSpace($MemoryRoot)) {
    $CliArgs += @('--memory-root', $MemoryRoot)
}
if (-not [string]::IsNullOrWhiteSpace($Type)) {
    $CliArgs += @('--type', $Type.ToLowerInvariant())
}
if ($PSBoundParameters.ContainsKey('Title')) {
    $CliArgs += @('--title', $Title)
}
if ($PSBoundParameters.ContainsKey('Content')) {
    $CliArgs += @('--content', $Content)
}
if ($PSBoundParameters.ContainsKey('TargetFile')) {
    $CliArgs += @('--target-file', $TargetFile)
}
if ($PSBoundParameters.ContainsKey('Query')) {
    $CliArgs += @('--query', $Query)
}
if (-not [string]::IsNullOrWhiteSpace($Status)) {
    $CliArgs += @('--status', $Status.ToLowerInvariant())
}
if ($PSBoundParameters.ContainsKey('Limit')) {
    $CliArgs += @('--limit', $Limit)
}
if ($PSBoundParameters.ContainsKey('RequireObsidian')) {
    $CliArgs += @('--require-obsidian', $RequireObsidian.ToLowerInvariant())
}
if ($PSBoundParameters.ContainsKey('ExperienceMode')) {
    $CliArgs += @('--experience-mode', $ExperienceMode.ToLowerInvariant())
}

& $PythonCommand @CliArgs
exit $LASTEXITCODE
