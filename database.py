from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)


def create_tables():
    """
    Create all database tables defined in models.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency that provides a database session.
    """
    with Session(engine) as session:
        yield session