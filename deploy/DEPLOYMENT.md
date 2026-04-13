# Gunicorn and Nginx Deployment

These files assume the app lives at:

```text
/var/www/cybersecurity-tools-webapp
```

## Server Setup

```bash
sudo apt update
sudo apt install -y python3 python3-venv nginx
cd /var/www/cybersecurity-tools-webapp
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Gunicorn

Copy the service file:

```bash
sudo cp deploy/gunicorn.service /etc/systemd/system/cybersecurity-tools-webapp.service
sudo systemctl daemon-reload
sudo systemctl enable cybersecurity-tools-webapp
sudo systemctl start cybersecurity-tools-webapp
sudo systemctl status cybersecurity-tools-webapp
```

## Nginx

Edit `deploy/nginx.conf` and replace `your-domain.example`.

Then copy and enable it:

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/cybersecurity-tools-webapp
sudo ln -s /etc/nginx/sites-available/cybersecurity-tools-webapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Production Check

```bash
curl -I http://127.0.0.1:8000
curl -I http://your-domain.example
```
