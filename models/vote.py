from typing import Optional
from sqlmodel import Field, SQLModel, Session, select, and_, func, Enum, Index
from config.database import engine
from pydantic import validator


class VoteValue(str, Enum):
    yes = "yes"
    no = "no"


class VoteStatus(str, Enum):
    valid = "valid"
    invalid = "invalid"


class Vote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: VoteValue
    status: VoteStatus

    @validator("value", pre=True, always=True)
    def validate_value(cls, value):
        if VoteValue.__dict__.get(value) is None:
            raise ValueError(f"Invalid value for vote: {value}")
        return VoteValue(value)

    @validator("status", pre=True, always=True)
    def validate_status(cls, status):
        if VoteStatus.__dict__.get(status) is None:
            raise ValueError(f"Invalid status: {status}")
        return VoteStatus(status)


def create_vote_query(engine: engine, vote: Vote) -> Vote:
    """_summary_

    Args:
        engine (engine): The database engine.
        vote (Vote): The vote to be created.

    Returns:
        vote (Vote): The vote that was created.
    """
    with Session(engine) as session:
        session.add(vote)
        session.commit()
        session.refresh(vote)
        return vote


def get_votes_query(engine: engine) -> list[dict]:
    """Fetches all votes from the database.

    Args:
        engine (engine): The database engine.

    Returns:
        votes (List[dict]): A list of votes.
    """
    with Session(engine) as session:
        votes = session.exec(select(Vote)).all()
        return [vote.dict() for vote in votes]  # Convert Vote objects to dictionaries


def get_vote_counts_query(engine: engine) -> dict[str, int]:
    """Counts the number of 'yes' and 'no' votes with a status of 'valid'.

    Args:
        engine (engine): The database engine.

    Returns:
        dict[str, int]: A dictionary with counts of 'yes' and 'no' votes.
    """
    with Session(engine) as session:
        yes_count = session.execute(
            select(func.count()).where(
                and_(Vote.value == "yes", Vote.status == "valid")
            )
        ).scalar()
        no_count = session.execute(
            select(func.count()).where(and_(Vote.value == "no", Vote.status == "valid"))
        ).scalar()
        return {"yes": yes_count, "no": no_count}
