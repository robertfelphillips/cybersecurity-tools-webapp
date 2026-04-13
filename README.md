# Cybersecurity Tools Web App

A Flask-based cybersecurity tools platform with a retro terminal interface. The app runs locally for development and is structured for later deployment behind Gunicorn and Nginx.

## Features

- Hash generator with SHA-256, SHA-512, SHA-1, and MD5 options.
- Base64 encoder/decoder with invalid-input handling.
- Controlled port scanner with permission confirmation and a 100-port scan limit.
- Log parser for IP extraction, HTTP status counts, failed-login detection, and suspicious event summaries.
- Production health check at `/health`.

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
samples/
tests/
requirements.txt
README.md
```

## Local Setup

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

## Tool Routes

```text
/              Hash generator
/base64        Base64 encoder/decoder
/port-scanner  Controlled port scanner
/log-parser    Log parser
/health        JSON health check
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

The tests cover:

- Hash generation
- Base64 encoding/decoding
- Invalid Base64 handling
- Port scanner validation and mocked open/closed ports
- Log parser counts, summaries, and file uploads
- Flask route availability
- Health check response

## Safety Notes

The port scanner is intentionally limited. Only scan systems you own or have explicit permission to test. The scanner requires a permission checkbox and limits each scan to 100 ports.

## Deployment Shape

```text
User -> Nginx -> Gunicorn -> Flask -> Tool logic
```

Install dependencies on the server:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Run with Gunicorn:

```bash
gunicorn -c deploy/gunicorn.conf.py app.app:app
```

Example Nginx reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.example;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Full deployment files are in `deploy/`:

```text
deploy/DEPLOYMENT.md
deploy/gunicorn.conf.py
deploy/gunicorn.service
deploy/nginx.conf
deploy/nginx-wsl-local.conf
```

## Future Improvements

- Add export buttons for scan and parser reports.
- Add authentication before exposing the app on a public server.
- Add rate limiting before public deployment.
