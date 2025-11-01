# Setup Guide - AI ROI Analytics Platform

## Prerequisites

Before you begin, ensure you have the following installed:

- Docker & Docker Compose (recommended)
- OR:
  - Python 3.11+
  - Node.js 18+
  - PostgreSQL 14+
  - Redis 7+

## Quick Start with Docker (Recommended)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd RoAI
```

### 2. Configure Environment Variables

**Backend:**
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and update:
- `SECRET_KEY` - Generate a secure random key (minimum 32 characters)
- Database credentials (if different from defaults)
- API keys for integrations (Google, Microsoft, OpenAI, etc.)

**Frontend:**
```bash
cp frontend/.env.example frontend/.env.local
```

### 3. Build and Start Services

```bash
# Build all containers
make build

# Start all services
make up

# View logs
make logs
```

This will start:
- **PostgreSQL** (TimescaleDB) on port 5432
- **Redis** on port 6379
- **Backend API** on port 8000
- **Frontend** on port 3000
- **Celery Worker** (background tasks)

### 4. Access the Application

- Frontend: http://localhost:3000
- Backend API Docs: http://localhost:8000/api/v1/docs
- Backend Health: http://localhost:8000/health

### 5. Initialize the Database

```bash
# Run migrations
make migrate

# Or manually:
docker-compose exec backend alembic upgrade head
```

## Manual Setup (Without Docker)

### Backend Setup

1. **Create Python Virtual Environment**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure Environment**

```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Start PostgreSQL and Redis**

Ensure PostgreSQL and Redis are running:
```bash
# PostgreSQL should be accessible at localhost:5432
# Redis should be accessible at localhost:6379
```

5. **Run Database Migrations**

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

6. **Start the Backend**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. **Start Celery Worker (Optional)**

In a separate terminal:
```bash
celery -A app.celery_app worker --loglevel=info
```

### Frontend Setup

1. **Install Dependencies**

```bash
cd frontend
npm install
```

2. **Configure Environment**

```bash
cp .env.example .env.local
# Edit .env.local if needed
```

3. **Start Development Server**

```bash
npm run dev
```

4. **Build for Production**

```bash
npm run build
npm start
```

## Database Setup

### TimescaleDB Extension

For time-series metrics optimization, enable TimescaleDB:

```sql
-- Connect to your database
psql -U roai_user -d roai_db

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Convert tables to hypertables (for time-series optimization)
SELECT create_hypertable('metric_snapshots', 'created_at');
SELECT create_hypertable('ai_tool_usage', 'created_at');
```

### Initial Data

To create a test organization and user:

```bash
# Using the API
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "securepassword123",
    "full_name": "Admin User",
    "organization_name": "Example Corp"
  }'
```

## Integration Setup

### Google Workspace

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable APIs:
   - Gmail API
   - Google Calendar API
   - Google Drive API
   - Google Sheets API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:8000/api/v1/integrations/google/callback`
6. Add credentials to `.env`:
   ```
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

### Microsoft 365

1. Go to [Azure Portal](https://portal.azure.com/)
2. Register a new application in Azure AD
3. Add Microsoft Graph API permissions:
   - Mail.Read
   - Calendars.Read
   - Files.Read.All
4. Create a client secret
5. Add credentials to `.env`:
   ```
   MICROSOFT_CLIENT_ID=your-client-id
   MICROSOFT_CLIENT_SECRET=your-client-secret
   MICROSOFT_TENANT_ID=your-tenant-id
   ```

### OpenAI

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an API key
3. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```

### Anthropic

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. Add to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

## Testing

### Backend Tests

```bash
# Run all tests
make test

# Or manually:
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Useful Commands

### Docker Commands

```bash
# View all services status
docker-compose ps

# Restart a specific service
docker-compose restart backend

# View backend logs
docker-compose logs -f backend

# Execute command in backend container
docker-compose exec backend python

# Access database
make db-shell

# Clean everything (WARNING: deletes data)
make clean
```

### Database Commands

```bash
# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# Apply migrations
make migrate

# Rollback one migration
docker-compose exec backend alembic downgrade -1

# View migration history
docker-compose exec backend alembic history
```

## Troubleshooting

### Backend won't start

1. Check PostgreSQL is running: `docker-compose ps postgres`
2. Check database URL in `.env` is correct
3. View backend logs: `docker-compose logs backend`

### Frontend can't connect to backend

1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
3. Check CORS settings in `backend/app/core/config.py`

### Database connection errors

1. Ensure PostgreSQL is running
2. Check credentials in `.env`
3. Test connection: `psql -U roai_user -d roai_db -h localhost`

### Port conflicts

If ports 3000, 8000, 5432, or 6379 are already in use:

1. Stop the conflicting service
2. Or modify ports in `docker-compose.yml`

## Security Notes

1. **Change SECRET_KEY**: Generate a strong random key for production
2. **Use environment variables**: Never commit `.env` files
3. **HTTPS in production**: Use a reverse proxy (Nginx, Traefik)
4. **Secure credentials**: Use secrets management (AWS Secrets Manager, HashiCorp Vault)
5. **Database backups**: Set up regular automated backups

## Next Steps

1. ✅ Set up integrations (Google, Microsoft, AI platforms)
2. ✅ Configure first organization
3. ✅ Add users
4. ✅ Connect external tools
5. ✅ Start collecting metrics
6. ✅ View analytics dashboards

## Support

For issues and questions:
- Check the documentation in `/docs`
- Review API docs at http://localhost:8000/api/v1/docs
- Open an issue on GitHub
