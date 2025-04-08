# LUSID Python SDK Local Dev Setup

This guide walks you through setting up a secure, reproducible local environment for working with the Finbourne LUSID Python SDK (v2), using tools `uv` for dependency management and `1Password` for secrets management.

---

## Prerequisites

Before you begin, ensure you have the following installed:

### 1. Python (>=3.10)
Install from https://www.python.org/

### 2. [1Password CLI (`op`)](https://developer.1password.com/docs/cli/get-started/)
Follow the instructions on the above page to get set up using 1passwordCLI

### 3. Install `uv`
```powershell
pip install uv
```

---

## Step-by-Step Setup

### 1. Create a Secure Item in 1Password

Use the CLI or UI to store your LUSID secrets (if you havent generated a secrets file yet, follow [this Knowledge Base Article (`op`)](https://support.lusid.com/docs/how-do-i-generate-and-reveal-a-client-secret?highlight=secrets).

```powershell
op item create --title "yourname@yourdomain" `
  username="your@email.com" `
  clientId="your-client-id" `
  clientSecret="your-client-secret" `
  password="your-lusid-password"
  tokenUrl="your-token-url"
```

---

### 2. Save `wla.ps1` in Project Folder

Create a file called `wla.ps1`:

```powershell
$fieldToEnvVarMap = @{
    "username"      = "FBN_LUSID_USER"
    "accessToken"   = "FBN_ACCESS_TOKEN"
    "clientId"      = "FBN_LUSID_CLIENT_ID"
    "clientSecret"  = "FBN_LUSID_CLIENT_SECRET"
    "password"      = "FBN_LUSID_PASSWORD"
}

if ($args.Count -lt 2) {
    Write-Host "Usage: .\wla.ps1 <itemName> <commandline...>"
    exit 1
}
$itemName = $args[0]
$command = $args[1]
$commandArgs = $args[2..$args.Count]

$secret = & op item get $itemName --format json | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to fetch secret from 1Password. Exiting."
    exit $LASTEXITCODE
}

foreach ($field in $secret.fields) {
    if ($field.value -and $field.label -and $fieldToEnvVarMap.ContainsKey($field.label)) {
        $envVarName = $fieldToEnvVarMap[$field.label]
        [System.Environment]::SetEnvironmentVariable($envVarName, $field.value, "Process")
    }
}

$dom = ($itemName -split "@")[1]
$base = "https://$dom.lusid.com"
$envVars = @{
    "FBN_LUSID_ENV"       = "$base"
    "FBN_LUSID_API_URL"   = "$base/api"
    "FBN_ACCESS_API_URL"  = "$base/access"
    "FBN_DRIVE_API_URL"   = "$base/drive"
}
foreach ($key in $envVars.Keys) {
    [System.Environment]::SetEnvironmentVariable($key, $envVars[$key], "Process")
}

Write-Host "Executing command: $($command + $commandArgs -join ' ')"
& $command $commandArgs
exit $LASTEXITCODE
```

---

### 3. Alias the `wla` Command

Open PowerShell profile:

```powershell
if (!(Test-Path -Path (Split-Path -Parent $PROFILE))) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $PROFILE)
}
if (!(Test-Path $PROFILE)) {
    New-Item -Path $PROFILE -ItemType File -Force
}
notepad $PROFILE
```

Add this line:
```powershell
Set-Alias wla "C:\path\to\your\project\wla.ps1"
```

Restart terminal.

---

### 4. Define Your Dependencies: `pyproject.toml`

Create this file in your project root:

```toml
[project]
name = "lusid-local-env"
version = "0.1.0"
description = "Local LUSID SDK v2 dev environment"
requires-python = ">=3.10"

dependencies = [
    "lusid-sdk==2.*",
    "finbourne-sdk-utils",
    "pandas",
    "jupyter"
]
```

---

### 5. Install Everything

From the project directory:
```powershell
wla yourname@yourdomain uv pip install
```

This installs and locks your dependencies in `uv.lock`.

---

### 6. Run LUSID Code

Create `main.py`:

```python
from lusid import SyncApiClientFactory, EnvironmentVariablesConfigurationLoader
from lusid.api import ApplicationMetadataApi
import pandas as pd

config_loaders = [EnvironmentVariablesConfigurationLoader()]
factory = SyncApiClientFactory(config_loaders=config_loaders)
metadata_api = factory.build(ApplicationMetadataApi)

lusid_versions = metadata_api.get_lusid_versions()
df = pd.DataFrame(lusid_versions.to_dict())
print(df)
```

Run it:
```powershell
wla yourname@yourdomain uv python main.py
```

---

### Optional: VS Code
To launch VS Code with all env vars:
```powershell
wla yourname@yourdomain code .
```

---

## You're Done 


