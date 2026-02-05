# Smart Emergency Healthcare Coordination System

A full-stack intelligent healthcare coordination platform.

## Tech Stack
- **Frontend**: React, Vite, Tailwind CSS, Leaflet Maps
- **Backend**: FastAPI, SQLite, SQLAlchemy, WebSockets
- **AI Engine**: Rule-based Hospital Readiness Scoring

## Setup Instructions

### 1. Backend Setup
1. Navigate to the `backend` directory.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   Server will start at `http://localhost:8000`. API Docs at `http://localhost:8000/docs`.

### 2. Frontend Setup
1. Navigate to the `frontend` directory.
2. Install dependencies (if not already done):
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   App will be available at `http://localhost:5173`.

## Usage
1. **Register**: Create an account (Patient, Hospital Admin, Ambulance, etc.).
2. **Hospital Admin**: Log in and "Register New Hospital" to add readiness data.
3. **Patient**: Log in and click "SOS" to request emergency help.
4. **AI Logic**: The system automatically assigns the best hospital based on distance and readiness score.
