param(
    [Parameter(Mandatory = $true)]
    [string]$EnvFile
)

if (-not (Test-Path -LiteralPath $EnvFile)) {
    Write-Error "Environment file '$EnvFile' not found."
    exit 1
}

$commentOrEmpty = '^[\s]*($|#)'

Get-Content -LiteralPath $EnvFile |
    Where-Object { $_ -notmatch $commentOrEmpty } |
    ForEach-Object {
        $line = $_.Trim()
        if (-not $line) { return }

        $equalsIndex = $line.IndexOf('=')
        if ($equalsIndex -lt 0) { return }

        $key = $line.Substring(0, $equalsIndex).Trim()
        $key = $key -replace '^export\s+', ''
        if (-not $key) { return }

        $value = $line.Substring($equalsIndex + 1).Trim()
        if ($value.Length -ge 2) {
            if (($value.StartsWith('"') -and $value.EndsWith('"')) -or
                ($value.StartsWith("'") -and $value.EndsWith("'"))) {
                $value = $value.Substring(1, $value.Length - 2)
            }
        }

        $value = $value -replace '`', '``'
        $value = $value -replace '"', '`"'

        Write-Output "`$Env:$key = \"$value\""
    }
