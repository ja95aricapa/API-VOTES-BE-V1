from typing import Optional
from sqlmodel import Field, SQLModel, Session, select, and_, func
from config.database import engine


class Vote(SQLModel, table=True):
    """
    Defines the Vote model for representing a Vote Table.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    value: str
    status: str


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


def get_votes_query(engine: engine) -> list[Vote]:
    """Fetches all votes from the database.

    Args:
        engine (engine): The database engine.

    Returns:
        votes (List[Vote]): A list of votes.
    """
    with Session(engine) as session:
        votes = session.exec(select(Vote)).all()
        return votes


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
