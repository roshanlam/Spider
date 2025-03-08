import asyncio
import threading
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from starlette.websockets import WebSocketState
from spider.plugin import Plugin

# Global metrics store and a set of connected WebSocket clients.
metrics_data = {
    "queueSize": 0,
    "crawled": 0,
    "errors": 0,
    "performance": 0,
    "timestamp": 0,
}
connected_clients = set()

app = FastAPI()

@app.get("/api/metrics")
async def get_metrics():
    """Return the current crawl metrics."""
    return metrics_data

@app.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint to push live metrics updates."""
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        connected_clients.discard(websocket)

async def broadcast_metrics(new_metrics: dict):
    """
    Update the global metrics_data and send the new metrics as JSON to all connected clients.
    Checks if a client is still connected before sending.
    """
    metrics_data.update(new_metrics)
    for client in list(connected_clients):
        if client.client_state != WebSocketState.CONNECTED:
            connected_clients.discard(client)
            continue
        try:
            await client.send_json(new_metrics)
        except Exception:
            connected_clients.discard(client)

class RealTimeMetricsPlugin(Plugin):
    def __init__(self, host: str = "0.0.0.0", port: int = 3001):
        self.host = host
        self.port = port
        # Start the FastAPI server in a background thread.
        thread = threading.Thread(target=self.run_server, daemon=True)
        thread.start()

    def run_server(self):
        uvicorn.run(app, host=self.host, port=self.port, log_level="info")

    async def should_run(self, url: str, content: str) -> bool:
        return True

    async def process(self, url: str, content: str) -> str:
        """
        Simulates a metrics update based on the URL's length and broadcasts the updated metrics
        via WebSocket. Returns the content unmodified.
        """
        new_metrics = {
            "queueSize": len(url) % 50,
            "crawled": (len(url) + 10) % 100,
            "errors": len(url) % 5,
            "performance": 100 - (len(url) % 20),
            "timestamp": int(time.time() * 1000)
        }
        # Schedule asynchronous broadcast without blocking.
        asyncio.create_task(self.async_broadcast(new_metrics))
        return content

    async def async_broadcast(self, new_metrics: dict):
        await broadcast_metrics(new_metrics)
