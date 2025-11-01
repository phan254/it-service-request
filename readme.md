# IT Service Request System

Flask-based web application for managing IT service requests.

## Features
- Submit IT service requests (public)
- Admin dashboard with statistics
- Request management (mark as resolved)
- REST API endpoints
- MySQL database integration
- External API integration for departments

## Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env .env
# Edit .env with your MySQL credentials
```

4. Create database:
```bash
mysql -u root -p < create_db.sql
```

5. Run application:
```bash
python app.py
```

6. Access:
- Public: https://luyaka.pythonanywhere.com/
- Admin: https://luyaka.pythonanywhere.com/admin/dashboard
- Credentials: admin/admin123

## API Endpoints

- `GET /api/requests` - List all requests
- `GET /api/requests?status=Pending` - Filter by status

## Database Schema

Table: requests
- id (INT, Primary Key)
- requester_name (VARCHAR 255)
- department (VARCHAR 255)
- category (VARCHAR 100)
- description (TEXT)
- status (VARCHAR 50, default 'Pending')
- created_at (DATETIME)
- resolved_at (DATETIME, nullable)

## Automation
- Auto-set status to "Pending" on submission
- Auto-timestamp when marked as resolved

## Deployment
Supports Render, PythonAnywhere, Railway. See hosting documentation.

---
**Name**: [Phanuel Disi]
**Experience**: [3 years]

**Repository**: [https://github.com/phan254/it-service-request]

