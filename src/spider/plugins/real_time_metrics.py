import asyncio
import threading
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from plugin import Plugin

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
            # Keep the connection alive.
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast_metrics(new_metrics: dict):
    """
    Update the global metrics_data and send the new metrics as JSON to all connected clients.
    If a client is closed, remove it from the list.
    """
    metrics_data.update(new_metrics)
    for client in list(connected_clients):
        try:
            await client.send_json(new_metrics)
        except RuntimeError:
            # The client is closed; remove it.
            connected_clients.remove(client)

class RealTimeMetricsPlugin(Plugin):
    """
    A real-time WebSocket plugin that starts a FastAPI server with:
      - A REST API endpoint (/api/metrics) for retrieving metrics.
      - A WebSocket endpoint (/ws/metrics) for live updates.
    """
    def __init__(self, host: str = "0.0.0.0", port: int = 3001):
        self.host = host
        self.port = port
        # Start the FastAPI server in a background thread.
        thread = threading.Thread(target=self.run_server, daemon=True)
        thread.start()

    def run_server(self):
        uvicorn.run(app, host=self.host, port=self.port, log_level="info")

    def process(self, url: str, content: str) -> str:
        """
        For each processed URL, simulate a metrics update (replace with real metrics)
        and broadcast the metrics via WebSocket.
        """
        import time
        new_metrics = {
            "queueSize": len(url) % 50,
            "crawled": (len(url) + 10) % 100,
            "errors": len(url) % 5,
            "performance": 100 - (len(url) % 20),
            "timestamp": int(time.time() * 1000)
        }
        # Schedule the asynchronous broadcast.
        asyncio.create_task(self.async_broadcast(new_metrics))
        return content

    async def async_broadcast(self, new_metrics: dict):
        await broadcast_metrics(new_metrics)
