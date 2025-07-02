# LUSID Python SDK Local Dev Setup - Windows Powershell

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
### 4. Install vscode

### 5. Install git

---

## Step-by-Step Setup

### 1. Create a Secure Item in 1Password

Use the CLI or UI to store your LUSID secrets (if you havent generated a secrets file yet, follow [this Knowledge Base Article](https://support.lusid.com/docs/how-do-i-generate-and-reveal-a-client-secret?highlight=secrets).

```powershell
op item create --title "yourname@yourdomain" `
  username="your@email.com" `
  clientId="your-client-id" `
  clientSecret="your-client-secret" `
  password="your-lusid-password"
  accessToken="your personal access token"
```

---

### 2. Save `wla.ps1` from auth-helpers in a designated Scripts folder on your device, i.e. "C:\Users\Name\Documents\Scripts" and create alias as instructed there


Add this line:
```powershell
Set-Alias wla "C:\path\to\your\scripts\wla.ps1"
```

Restart terminal.

---
### 3. Go to your repository with a dependencies file, and run command :
```powershell
uv init
```




