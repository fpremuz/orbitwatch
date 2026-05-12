from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        self.active_connections: list[WebSocket] = []


    async def connect(
        self,
        websocket: WebSocket,
    ):

        await websocket.accept()

        self.active_connections.append(
            websocket
        )

        print(
            f"Client connected. Total: {len(self.active_connections)}"
        )


    def disconnect(
        self,
        websocket: WebSocket,
    ):

        if websocket in self.active_connections:

            self.active_connections.remove(
                websocket
            )

        print(
            f"Client disconnected. Total: {len(self.active_connections)}"
        )


    async def broadcast(
        self,
        message: dict,
    ):

        print("BROADCASTING MESSAGE")
        print(message)
        print(f"Connected clients: {len(self.active_connections)}")

        disconnected = []

        for connection in self.active_connections:

            try:

                await connection.send_json(
                    message
                )

            except Exception:

                disconnected.append(
                    connection
                )

        for connection in disconnected:

            self.disconnect(connection)


manager = ConnectionManager()