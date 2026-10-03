from collections import defaultdict
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter(
    tags=["WebSocket"],
)


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: list[WebSocket] = []
        self.task_connections: dict[str, list[WebSocket]] = defaultdict(
            list
        )

    async def connect(
        self,
        websocket: WebSocket,
        task_id: str | None = None,
    ) -> None:
        await websocket.accept()

        self.connections.append(websocket)

        if task_id:
            self.task_connections[task_id].append(websocket)

    def disconnect(
        self,
        websocket: WebSocket,
        task_id: str | None = None,
    ) -> None:
        if websocket in self.connections:
            self.connections.remove(websocket)

        if task_id and websocket in self.task_connections.get(
            task_id,
            [],
        ):
            self.task_connections[task_id].remove(websocket)

    async def broadcast(
        self,
        event: dict[str, Any],
    ) -> None:
        disconnected = []

        for websocket in self.connections:
            try:
                await websocket.send_json(event)
            except Exception:
                disconnected.append(websocket)

        for websocket in disconnected:
            self.disconnect(websocket)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):
    await manager.connect(websocket)

    try:
        await websocket.send_json(
            {
                "type": "connection.ready",
                "message": "AMY WebSocket connected.",
            }
        )

        while True:
            message = await websocket.receive_json()

            if message.get("type") == "ping":
                await websocket.send_json(
                    {
                        "type": "pong",
                    }
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)