# Windows/PowerShell runtime behavior is unverified.
[CmdletBinding()]
param(
    [ValidateSet('codex', 'claude')][string]$Agent = 'codex',
    [string]$Destination
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Assert-PlainPath([string]$Path) {
    $part = $Path
    while ($part) {
        $item = Get-Item -LiteralPath $part -Force -ErrorAction SilentlyContinue
        if ($item -and ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Reparse/symlink path left untouched: $part. Choose its real location."
        }
        $part = [IO.Path]::GetDirectoryName($part)
    }
}

$profilePath = [Environment]::GetFolderPath('UserProfile')
if (-not $Destination) {
    $agentFolder = if ($Agent -eq 'claude') { '.claude' } else { '.agents' }
    $Destination = Join-Path (Join-Path $profilePath $agentFolder) 'skills'
}
if (-not [IO.Path]::IsPathRooted($Destination)) { throw 'Destination must be an absolute skills parent directory.' }
$parentPath = [IO.Path]::GetFullPath($Destination)
if ($parentPath.TrimEnd('\', '/') -eq [IO.Path]::GetPathRoot($parentPath).TrimEnd('\', '/')) {
    throw 'The skills parent directory must not be a filesystem root.'
}
$targetPath = Join-Path $parentPath 'edit-my-app'
Assert-PlainPath $targetPath
if (Test-Path -LiteralPath $targetPath) {
    Write-Output "Already exists; left untouched: $targetPath. Move this skill aside before updating it."
    return
}
$files = @('SKILL.md', 'references/workflow.md', 'references/tools.md', 'references/macos.md',
    'references/ios.md', 'references/windows.md', 'references/linux.md', 'references/android.md', 'LICENSE')
$sourcePath = if ($PSScriptRoot) { Join-Path $PSScriptRoot 'skills/edit-my-app' } else { $null }
$localSource = $sourcePath -and (Test-Path -LiteralPath $sourcePath -PathType Container)
if ($sourcePath -and -not $localSource) { throw 'The local checkout is incomplete. Use the remote install command or a complete checkout.' }
[IO.Directory]::CreateDirectory($parentPath) | Out-Null
$stagePath = Join-Path $parentPath ('.edit-my-app-stage.' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stagePath | Out-Null
try {
    $payloadPath = Join-Path $stagePath 'edit-my-app'
    [IO.Directory]::CreateDirectory((Join-Path $payloadPath 'references')) | Out-Null
    foreach ($file in $files) {
        $toPath = Join-Path $payloadPath $file
        if ($localSource) {
            $fromPath = Join-Path $sourcePath $file
            Assert-PlainPath $fromPath
            $fromItem = Get-Item -LiteralPath $fromPath
            if ($fromItem.PSIsContainer -or $fromItem.Length -eq 0) { throw "Invalid skill file: $file" }
            Copy-Item -LiteralPath $fromPath -Destination $toPath
        }
        else {
            $uri = "https://raw.githubusercontent.com/Pasta-Lab/edit-my-app/main/skills/edit-my-app/$file"
            Invoke-WebRequest -UseBasicParsing -Uri $uri -OutFile $toPath
            if (-not (Test-Path -LiteralPath $toPath -PathType Leaf) -or (Get-Item -LiteralPath $toPath).Length -eq 0) {
                throw "Download was empty or invalid: $file"
            }
        }
    }
    $header = Get-Content -LiteralPath (Join-Path $payloadPath 'SKILL.md') -Raw
    if ($header -notmatch '(?m)^name: edit-my-app\r?$' -or -not $header.StartsWith('---')) {
        throw 'Unexpected skill metadata.'
    }
    # Directory.Move fails if the destination already exists; never overwrite.
    [IO.Directory]::Move($payloadPath, $targetPath)
    Write-Output "Installed Edit My App: $targetPath"
    Write-Output 'No apps, analysis tools, SDKs, or agent settings were changed.'
    Write-Output 'Start a new agent chat and say: Use edit-my-app to change my app.'
}
finally {
    # This exact, newly created staging directory contains only our own copies.
    Assert-PlainPath $stagePath
    if (Test-Path -LiteralPath $stagePath) { Remove-Item -LiteralPath $stagePath -Recurse -Force }
}
