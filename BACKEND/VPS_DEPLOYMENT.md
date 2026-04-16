# Backend VPS Deployment

This guide is for deploying only the backend to a VPS, without Cloudflare and without a real domain yet.

## Backend VPS Only

Remove all Cloudflare steps and all hardcoded domain references for now.

Important: `Let's Encrypt` cannot issue a certificate for a bare server IP. You need a real domain or subdomain pointing to your VPS before `Certbot` can create a valid SSL certificate.

For now, the correct setup is:

1. Deploy the backend on the VPS over HTTP.
2. When you later buy a domain, point it to the VPS.
3. Then enable HTTPS with `Nginx + Certbot`.

## Firewall

On the VPS, open HTTP now:

```bash
ufw allow 80/tcp
ufw reload
ufw status
```

If you later add SSL, also open HTTPS:

```bash
ufw allow 443/tcp
ufw reload
ufw status
```

## Run Backend On VPS

From the backend project directory:

```bash
docker compose up -d --build
```

Check containers:

```bash
docker compose ps
docker compose logs -f nginx
docker compose logs -f app
```

Your backend should then be reachable at:

```text
http://YOUR_VPS_PUBLIC_IP
```

If your API routes are under `/api`, test with:

```bash
curl http://YOUR_VPS_PUBLIC_IP/health
curl http://YOUR_VPS_PUBLIC_IP/api/...
```

## No SSL Yet

Do not run this yet:

```bash
certbot certonly --standalone ...
```

That only works after you have a domain such as `api.yourdomain.com` pointing to the VPS.

## Later: Enable SSL With Nginx/Certbot

Once you have a domain:

1. Create an `A` record pointing your domain or subdomain to the VPS IP.
2. Open both ports:

```bash
ufw allow 80/tcp
ufw allow 443/tcp
ufw reload
```

3. Install `certbot`:

```bash
apt update
apt install -y certbot
```

4. Stop Docker temporarily if port `80` is in use:

```bash
docker compose down
```

5. Issue certificate:

```bash
certbot certonly --standalone -d api.yourdomain.com
```

6. Certificates will be here:

```text
/etc/letsencrypt/live/api.yourdomain.com/
```

7. Then update Nginx to use those certificate files and restart Docker:

```bash
docker compose up -d --build
```

## Updating Backend After Changes

```bash
docker compose down
docker compose up -d --build
```

## Useful Commands

```bash
docker compose ps
docker compose logs -f nginx
docker compose logs -f app
docker image prune -f
```

## Auto Renew Later

Only after you have a domain and SSL configured:

```bash
crontab -e
```

Add:

```bash
0 0 * * * certbot renew --quiet && docker compose -f /path/to/your/docker-compose.yml restart nginx
```
