from repositories.interfaces import IRepository


class PostgresRepository(IRepository):
    """
    Repository for working with Postgres database
    """
    model = None

    def __init__(self, model) -> None:
        self.model = model

    def get(self) -> None:
        return None

    def create(self) -> None:
        return None

    def update(self) -> None:
        return None

    def delete(self) -> None:
        return None
