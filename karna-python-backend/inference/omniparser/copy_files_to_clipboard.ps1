# copy_files_to_clipboard.ps1
<#
.SYNOPSIS
    Copies one or more files to the clipboard (CF_HDROP format) so they can be pasted.

.DESCRIPTION
    This script accepts file paths via the -Files parameter or as positional arguments.
    It resolves each file path to its absolute form, verifies existence, and collects valid files.
    It then uses System.Windows.Forms.Clipboard to set the clipboard’s file drop list.

.PARAMETER Files
    One or more file paths to copy to the clipboard.

.EXAMPLE
    # Using the named parameter:
    .\copy_files_to_clipboard.ps1 -Files "C:\path\to\file1.txt","C:\path\to\file2.jpg"
    
.EXAMPLE
    # Using positional parameters:
    .\copy_files_to_clipboard.ps1 "C:\path\to\file1.txt" "C:\path\to\file2.jpg"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false, ValueFromRemainingArguments = $true)]
    [string[]]$Files
)

# Debug: starting execution
Write-Output "[DEBUG] Starting copy_files_to_clipboard.ps1..."

# If no files provided, exit with an error.
if (-not $Files -or $Files.Count -eq 0) {
    Write-Error "[DEBUG] No files provided. Exiting."
    exit 1
}

# Create a StringCollection to hold the valid absolute file paths.
$fileCollection = New-Object System.Collections.Specialized.StringCollection

foreach ($file in $Files) {
    # Try to resolve the file to an absolute path.
    $resolvedPath = Resolve-Path $file -ErrorAction SilentlyContinue
    if ($resolvedPath) {
        $resolvedFile = $resolvedPath.Path
        Write-Output "[DEBUG] Resolved file: $resolvedFile"
        $fileCollection.Add($resolvedFile) | Out-Null
    }
    else {
        Write-Warning "[DEBUG] File not found or cannot resolve: $file"
    }
}

Write-Output "[DEBUG] File collection count: $($fileCollection.Count)"

if ($fileCollection.Count -eq 0) {
    Write-Error "[DEBUG] No valid files found. Exiting."
    exit 1
}

try {
    # Load the System.Windows.Forms assembly.
    Add-Type -AssemblyName System.Windows.Forms
    # Set the clipboard file drop list.
    [System.Windows.Forms.Clipboard]::SetFileDropList($fileCollection)
    Write-Output "[DEBUG] Files copied to clipboard successfully."
}
catch {
    Write-Error "[DEBUG] Error occurred while copying files to clipboard: $_"
    exit 1
}
