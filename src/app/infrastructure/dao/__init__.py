from app.infrastructure.database import DatabaseWrapper


class BaseDAO:
    def __init__(self, db: DatabaseWrapper):
        self.db = db
