# Cybersecurity Tools Web App

A Flask-based cybersecurity tools dashboard with a retro terminal interface. It was built as a local-first security toolkit and can be deployed publicly through Render or on a Linux server with Gunicorn and Nginx.

## Live Demo

Add the Render URL here after deployment:

```text
https://your-render-app-name.onrender.com
```

## Features

- **Hash Generator**: generate SHA-256, SHA-512, SHA-1, and MD5 hashes.
- **Base64 Tool**: encode text to Base64 or decode valid Base64 back to text.
- **Controlled Port Scanner**: scan a limited port range after confirming permission.
- **Log Parser**: paste logs or upload `.log` / `.txt` files to extract IPs, HTTP status codes, failed login attempts, errors, warnings, and suspicious lines.
- **Production Health Check**: `/health` returns JSON for deployment monitoring.

## Tool Routes

```text
/              Hash generator
/base64        Base64 encoder/decoder
/port-scanner  Controlled port scanner
/log-parser    Log parser
/health        JSON health check
```

## Project Structure

```text
cybersecurity-tools-webapp/
app/
  app.py
  static/
    app.js
    styles.css
  templates/
  tools/
deploy/
  DEPLOYMENT.md
  RENDER.md
  gunicorn.conf.py
  gunicorn.service
  nginx.conf
  nginx-wsl-local.conf
samples/
tests/
render.yaml
requirements.txt
README.md
```

## Local Setup

Windows PowerShell:

```powershell
cd C:\Users\rober\OneDrive\Documents\Playground\cybersecurity-tools-webapp
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.app
```

Open:

```text
http://127.0.0.1:5000
```

## WSL / Gunicorn Test

Use this to confirm the app runs through Gunicorn before using Nginx:

```bash
cd /mnt/c/Users/rober/OneDrive/Documents/Playground/cybersecurity-tools-webapp
python3 -m venv .venv-linux
. .venv-linux/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests
gunicorn -c deploy/gunicorn.conf.py app.app:app
```

Open:

```text
http://127.0.0.1:8000
```

## WSL / Nginx Local Test

Install Nginx in WSL:

```bash
sudo apt update
sudo apt install -y nginx
```

Start Gunicorn in one WSL terminal:

```bash
cd /mnt/c/Users/rober/OneDrive/Documents/Playground/cybersecurity-tools-webapp
. .venv-linux/bin/activate
gunicorn -c deploy/gunicorn.conf.py app.app:app
```

In another WSL terminal, enable the local Nginx config:

```bash
cd /mnt/c/Users/rober/OneDrive/Documents/Playground/cybersecurity-tools-webapp
sudo cp deploy/nginx-wsl-local.conf /etc/nginx/sites-available/cybersecurity-tools-webapp-wsl
sudo ln -s /etc/nginx/sites-available/cybersecurity-tools-webapp-wsl /etc/nginx/sites-enabled/
sudo nginx -t
sudo service nginx reload
```

Open:

```text
http://127.0.0.1:8080
```

## Free Public Deployment With Render

This repo includes `render.yaml`, so Render can deploy the app directly from GitHub.

1. Go to Render.
2. Create a new Blueprint or Web Service from this repository.
3. Use the free plan.
4. Let Render detect `render.yaml`.
5. Deploy.

Render runs:

```bash
gunicorn -w 3 -b 0.0.0.0:$PORT app.app:app
```

Health check:

```text
/health
```

Public scanner safety is enabled in `render.yaml`:

```text
SCANNER_ALLOWED_HOSTS=127.0.0.1,localhost,::1
```

That prevents the hosted demo from being used to scan arbitrary internet hosts.

## Linux Server Deployment

The production path is:

```text
User -> Nginx -> Gunicorn -> Flask -> Tool logic
```

Full instructions are in:

```text
deploy/DEPLOYMENT.md
```

The included templates are:

```text
deploy/gunicorn.service
deploy/nginx.conf
```

## Manual Test Checklist

Hash generator:

```text
Input: hello
Algorithm: SHA-256
Expected: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

Base64:

```text
Encode hello -> aGVsbG8=
Decode aGVsbG8= -> hello
```

Port scanner:

```text
Host: 127.0.0.1
Start port: 1
End port: 100
Check the permission box before scanning.
```

Log parser:

```text
Use samples/sample-auth.log or samples/sample-web.log.
You can paste log text or upload a .log/.txt file up to 1 MB.
```

## Automated Tests

Run:

```powershell
.\.venv\Scripts\python -m unittest discover -s tests
```

Or in WSL:

```bash
python -m unittest discover -s tests
```

The tests cover:

- Hash generation
- Base64 encode/decode behavior
- Invalid Base64 handling
- Log parsing and file upload handling
- Port scanner validation and mocked port states
- Flask page routes
- `/health` response

## Safety Notes

Only scan systems you own or have explicit permission to test. The scanner is intentionally limited to 100 ports per scan and includes a permission confirmation step.

For public deployments, set:

```text
SCANNER_ALLOWED_HOSTS=127.0.0.1,localhost,::1
```

Leave it unset during trusted local development if you need to scan another approved host.

## Future Improvements

- Add screenshots after the Render URL is live.
- Add export buttons for scan and parser reports.
- Add authentication before exposing private/internal tools.
- Add rate limiting before heavier public use.
