# 🚀 Quick Start Guide

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ installed
- MySQL database (or PlanetScale account)

## Step-by-Step Setup

### 1. Clone and Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy from .env.example and update with your database credentials
```

### 2. Setup Database

Create a MySQL database and update `DATABASE_URL` in `backend/.env`:
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/school_records
```

### 3. Run Backend

```bash
# From backend directory
uvicorn app:app --reload
```

Backend will be available at `http://localhost:8000`

### 4. (Optional) Seed Sample Data

```bash
# From backend directory
python seed_data.py
```

This creates:
- Admin: admin@school.com / admin123
- Teacher: teacher@school.com / teacher123
- Student: student@school.com / student123

### 5. Setup Frontend

```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install

# Create .env file
# Copy from .env.example and update API URL if needed
```

### 6. Run Frontend

```bash
# From frontend directory
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 🎉 You're Ready!

1. Open `http://localhost:3000` in your browser
2. Login with one of the seeded accounts
3. Explore the dashboards!

## Troubleshooting

### Backend Issues

- **Port already in use**: Change port in uvicorn command: `uvicorn app:app --reload --port 8001`
- **Database connection error**: Check your `DATABASE_URL` in `.env`
- **Import errors**: Make sure virtual environment is activated and dependencies are installed

### Frontend Issues

- **API connection error**: Check `VITE_API_BASE_URL` in `frontend/.env`
- **Build errors**: Delete `node_modules` and `package-lock.json`, then run `npm install` again
- **Port already in use**: Vite will automatically use the next available port

## Next Steps

- Check the main [README.md](README.md) for deployment instructions
- Review API documentation in backend routes
- Customize the theme colors in `frontend/tailwind.config.js`

