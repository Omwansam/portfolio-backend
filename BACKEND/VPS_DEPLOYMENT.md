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

1. Prepare deployment env vars:

```bash
nano .env
```

Set required values in `.env` (single source of truth):

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `CORS_ORIGINS` (use your frontend origin, or `*` temporarily)

Use a Docker-safe database URL on VPS, for example:

```env
DATABASE_URL=postgresql://arnold:Falcon%407ham@db:5432/portfolio
```

Important:
- `localhost:5433` works from your host machine.
- Inside Docker containers, `localhost` points to the container itself.
- For Docker deployment, use `db:5432` in `DATABASE_URL`.

1. Ensure the deployment files exist and are up to date:

- `docker-compose.yml`
- `Dockerfile`
- `entrypoint.sh`
- `nginx.conf`
- `.env` (local VPS file, do not commit)

1. Start services:

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

