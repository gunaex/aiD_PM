# Deployment Guide: Updating Your Application on OrbStack

Here are the steps to update your application after making changes.

## 1. Updating Code (Quick)
If you modify Python files (`.py`) or templates (`.html`):
1. Save your changes.
2. Restart the container to apply changes:
   ```bash
   docker compose restart
   ```
   *Note: Docker volume mounting means your file changes are already inside the container, but the server needs a restart to reload them.*

## 2. Adding New Libraries (Slow)
If you add new packages to `requirements.txt`:
1. Rebuild the image:
   ```bash
   docker compose up -d --build
   ```
   *This is necessary to install the new dependencies.*

## 3. Full Reset (Troubleshooting)
If something is broken and you want a clean slate (your data in `pm_system.db` will be safe):
1. Stop everything:
   ```bash
   docker compose down
   ```
2. Rebuild and start fresh:
   ```bash
   docker compose up -d --build --force-recreate
   ```

## Viewing Logs
To see if your changes caused any errors or to watch the server start:
```bash
docker compose logs -f
```
(Press `Ctrl+C` to exit logs)


FYI : Deployment successful! Your application is now running on OrbStack.

URL: http://localhost:8000
Container: aid_pm-web-1
Data Persistence: pm_system.db, backups_auto, and exports are preserved on your host machine.

---

## After Code Refactoring / New Features

When new code is added (like the On-Site / Discussion / Consensus Report feature), follow these steps:

### 1. Rebuild the Container
```bash
docker compose up -d --build
```
This rebuilds the image with your new code and restarts the container.

### 2. Run Database Migrations (if applicable)
If new database tables or columns were added, run the migration:
```bash
docker compose exec web python migrate_project_profiles.py
```
Or for the initial onsite reports migration:
```bash
docker compose exec web python migrate_onsite_reports.py
```

### 3. Verify the Application
Check that the server started successfully:
```bash
docker compose logs web --tail 20
```

### 4. Test the New Features
- Navigate to http://localhost:8000
- Test the new functionality
- For onsite reports: Go to any project → Settings → Configure company profiles

### Quick Reference
```bash
# Full refresh workflow
docker compose up -d --build
docker compose exec web python migrate_project_profiles.py
docker compose logs web --tail 20
```