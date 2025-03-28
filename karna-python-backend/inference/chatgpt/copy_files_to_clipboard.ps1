# copy_files_to_clipboard.ps1
<#
.SYNOPSIS
    Copies one or more files to the clipboard so they can be pasted (CF_HDROP format).

.DESCRIPTION
    This script accepts one or more file paths via the -Files parameter.
    If the –Files parameter isn’t used, it falls back to using any positional arguments.
    It verifies each file exists and then uses the System.Windows.Forms.Clipboard
    API to set the file drop list.

.PARAMETER Files
    One or more file paths to copy to the clipboard.
    
.EXAMPLE
    # Using the named parameter:
    .\copy_files_to_clipboard.ps1 -Files "C:\path\to\file1.txt","C:\path\to\file2.jpg"
    
.EXAMPLE
    # Using positional parameters:
    .\copy_files_to_clipboard.ps1 "C:\path\to\file1.txt" "C:\path\to\file2.jpg"
#>

param(
    [string[]]$Files
)

# Fallback: if -Files was not used, use the positional arguments
if (-not $Files -or $Files.Count -eq 0) {
    $Files = $args
}

if (-not $Files -or $Files.Count -eq 0) {
    Write-Error "[PS-DEBUG]: No files provided."
    exit 1
}

try {
    # Load the required .NET assembly
    Add-Type -AssemblyName System.Windows.Forms

    # Create a StringCollection and add each valid file path (resolved to absolute paths)
    $fileCollection = New-Object System.Collections.Specialized.StringCollection
    foreach ($file in $Files) {
        if (Test-Path $file) {
            $resolved = (Resolve-Path $file).Path
            $fileCollection.Add($resolved) | Out-Null
        }
        else {
            Write-Warning "[PS-DEBUG]: File not found: $file"
        }
    }

    if ($fileCollection.Count -eq 0) {
        Write-Error "[PS-DEBUG]: No valid files were provided."
        exit 1
    }

    # Set the file drop list (CF_HDROP format) on the clipboard
    # print the fileCollection length
    Write-Output "[PS-DEBUG]: File collection length: $($fileCollection.Count)"
    [System.Windows.Forms.Clipboard]::SetFileDropList($fileCollection)
    Write-Output "[PS-DEBUG]: Files copied to clipboard successfully."
}
catch {
    Write-Error "[PS-DEBUG]: An error occurred: $_"
}
