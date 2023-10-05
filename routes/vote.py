from models.vote import Vote
from fastapi import APIRouter, WebSocket
from config.database import engine
from services.vote import (
    create_vote_service,
    get_votes_service,
    get_vote_counts_service,
)

vote_router = APIRouter(tags=["Vote"], prefix="/v1")

# WebSocket route to provide real-time updates
connected_clients = []


@vote_router.post("/vote/")
async def create_vote_route(vote: Vote) -> Vote:
    """Endpoint to create a new vote.

    Args:
        vote (Vote): The vote object to be created.

    Returns:
        Vote: The created vote object.
    """
    new_vote = create_vote_service(engine=engine, vote=vote)
    if not connected_clients:
        return new_vote
    else:
        vote_counts = get_vote_counts_service(engine=engine)
        # send updated vote count to all connected clients
        disconnected_clients = []
        for client in connected_clients:
            try:
                await client.send_text(
                    vote_counts
                )  # Se asume que vote_counts es una cadena JSON
            except:
                disconnected_clients.append(client)
        # Remove disconnected clients
        for client in disconnected_clients:
            connected_clients.remove(client)
        return new_vote


@vote_router.get("/vote/")
def get_votes_route() -> list[dict]:
    """Endpoint to fetch all votes.

    Returns:
        list[dict]: A list of all vote objects.
    """
    votes = get_votes_service(engine=engine)
    return votes


@vote_router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint to provide real-time updates.

    Args:
        websocket (WebSocket): The WebSocket object.
    """
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "disconnect":
                await websocket.send_text(f"Disconnected")
                break
    except:
        pass
    finally:
        connected_clients.remove(websocket)
        await websocket.close()
