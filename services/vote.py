from models.vote import Vote, create_vote_query, get_votes_query, get_vote_counts_query
from fastapi import HTTPException, status
from config.database import engine
import json


def create_vote_service(engine: engine, vote: Vote) -> Vote:
    """Service to create a new vote.

    Args:
        engine (engine): The database engine.
        vote (Vote): The vote object to be created.

    Raises:
        HTTPException: An exception if the vote cannot be created.

    Returns:
        Vote: The created vote object.
    """
    try:
        new_vote = create_vote_query(engine=engine, vote=vote)
        return new_vote
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating vote, reason: {e}",
        )


def get_votes_service(engine: engine) -> list[dict]:
    """Service to fetch all votes.

    Args:
        engine (engine): The database engine.

    Raises:
        HTTPException: An exception if the votes cannot be fetched.

    Returns:
        list[dict]: A list of all vote objects.
    """
    try:
        votes = get_votes_query(engine=engine)
        return votes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error getting votes, reason: {e}",
        )


def get_vote_counts_service(engine: engine) -> dict[str, int]:
    """Service to count the number of 'yes' and 'no' votes.

    Args:
        engine (engine): The database engine.

    Raises:
        HTTPException: An exception if the vote counts cannot be fetched.

    Returns:
        dict[str, int]: A dictionary with counts of 'yes' and 'no' votes.
    """
    try:
        vote_counts = get_vote_counts_query(engine=engine)
        # Serialize vote data to JSON
        vote_counts_json = json.dumps(vote_counts)
        return vote_counts_json
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error getting vote counts, reason: {e}",
        )
