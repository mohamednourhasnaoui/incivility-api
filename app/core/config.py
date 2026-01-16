from sqlmodel import SQLModel, create_engine, Session

# Base de données en mémoire (SQLite)
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, echo=True)

# Crée toutes les tables automatiquement
def init_db():
    from app.models import report, category  # importe tous tes modèles
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
