from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import endpoints
from .services import websocket_manager

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Healthcare Emergency System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api")

@app.websocket("/ws")
async def websocket_endpoint(websocket: websocket_manager.WebSocket):
    await websocket_manager.manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except websocket_manager.WebSocketDisconnect:
        websocket_manager.manager.disconnect(websocket)
